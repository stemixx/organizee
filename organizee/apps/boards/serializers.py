from rest_framework import serializers
from .models import Board, BoardMember, CustomUser, Label


class BoardMemberSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=CustomUser.objects.all())

    class Meta:
        model = BoardMember
        fields = ('user', 'role')


class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    members = BoardMemberSerializer(many=True)

    class Meta:
        model = Board
        fields = '__all__'

    def create(self, validated_data):
        """
        Создание нового объекта Board. Если поле 'members' не передано,
        текущий пользователь автоматически становится администратором доски.
        """
        members_data = validated_data.pop('members', []) or [{'user': self.context['request'].user, 'role': 'admin'}]
        board = Board.objects.create(**validated_data)
        for member_data in members_data:
            BoardMember.objects.create(board=board, **member_data)
        return board

    def update(self, instance, validated_data):
        """
        Обновление существующего объекта Board. Обновляет поля 'name' и 'description'.
        Обновляет членов доски, добавляя новых, обновляя существующих и удаляя тех, кто не был передан,
        за исключением владельца доски.
        """
        # сохраняем переданные пользователем данные, автоматически обновляя поле updated_at
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # забираем новые данные о пользователях доски
        new_members_data = validated_data.pop('members', [])
        # создаём словарь текущих пользователей для последующей сверки
        current_members = {member.user.email: member for member in instance.members.all()}
        owner_email = instance.owner.email

        for new_member in new_members_data:
            user = new_member.get('user')
            role = new_member.get('role')

            # если пользователь был членом доски, обновляем данные о нём
            if user.email in current_members:
                member = current_members.pop(user.email)
                # данные о владельце, если они переданы, не меняем
                if user.email == owner_email:
                    continue
                member.role = role
                member.save()
            # если пользователь не был членом доски, то добавляем его
            else:
                BoardMember.objects.create(board=instance, user=user, role=role)

        # Удаляем текущих членов доски, которые не были в новых данных, кроме владельца
        for member in current_members.values():
            if member.user.email != owner_email:
                member.delete()

        return instance


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'name', 'color', 'board')
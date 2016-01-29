from django.contrib.auth.models import User, Group
from django.test import TestCase
from django_seed import Seed


class QTest(TestCase):
    def setUp(self):
        seeder = Seed.seeder()
        seeder.add_entity(User, 5)
        seeder.add_entity(Group, 3)

        inserted_pks = seeder.execute()
        user_pks = inserted_pks.get(User)
        group_pks = inserted_pks.get(Group)

        memberships = [
            (1, 1),
            (1, 2),
        ]

        for user_id, group_id in memberships:
            User.groups.through(user_id=user_pks[user_id], group_id=group_pks[group_id]).save()

    def test_setup(self):
        pass

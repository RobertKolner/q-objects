from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.test import TestCase
from django_seed import Seed


group_pks = []
user_pks = []


def q(n):
    return Q(groups__pk=group_pks[n])


def count(query):
    return User.objects.filter(query).distinct().count()


class QTest(TestCase):
    def setUp(self):
        seeder = Seed.seeder()
        seeder.add_entity(User, 1)
        seeder.add_entity(Group, 3)

        global group_pks
        global user_pks

        inserted_pks = seeder.execute()
        user_pks = inserted_pks.get(User)
        group_pks = inserted_pks.get(Group)

        memberships = [
            (0, [0, 1, 2]),
        ]

        for user_id, group_ids in memberships:
            for group_id in group_ids:
                user_pk = user_pks[user_id]
                group_pk = group_pks[group_id]
                User.groups.through(user_id=user_pk, group_id=group_pk).save()

    def test_setup(self):
        query_simple = q(0) & q(1) & q(2)
        query_neg = ~(~q(0) | ~q(1) | ~q(2))

        self.assertEqual(count(query_simple), count(query_neg))

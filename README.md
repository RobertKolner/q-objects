A minimal project to display an inconsistency with logic of Django's Q-objects and many-to-many relationships.
For instance, `Q(a) & Q(b)` is not equal to `~(~Q(a) | ~Q(b))`. Using default models from `django.contrib.auth`, we're
able to produce following queries:

```sql
-- Q(groups__pk=1) & Q(groups__pk=2)
SELECT DISTINCT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM "auth_user"
  INNER JOIN "auth_user_groups" ON ("auth_user"."id" = "auth_user_groups"."user_id")
WHERE ("auth_user_groups"."group_id" = 1 AND "auth_user_groups"."group_id" = 2);
```

...and...

```sql
-- ~(~Q(groups__pk=1) | ~Q(groups__pk=2))
SELECT DISTINCT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM "auth_user"
WHERE NOT ((NOT ("auth_user"."id" IN (SELECT U1."user_id" AS Col1
                                      FROM "auth_user_groups" U1
                                      WHERE U1."group_id" = 1))
            OR NOT ("auth_user"."id" IN (SELECT U1."user_id" AS Col1
                                         FROM "auth_user_groups" U1
                                         WHERE U1."group_id" = 2))
));
```

The second one returns the expected results. The first one is obviously wrong. An expected query could look like this:

```sql
-- Expected for Q(groups__pk=1) & Q(groups__pk=2)
SELECT DISTINCT 
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM "auth_user"
WHERE "auth_user"."id" IN (SELECT U1."user_id"
                           FROM "auth_user_groups" U1
                           WHERE U1."group_id" = 1)
      AND "auth_user"."id" IN (SELECT U1."user_id"
                               FROM "auth_user_groups" U1
                               WHERE U1."group_id" = 2)
```
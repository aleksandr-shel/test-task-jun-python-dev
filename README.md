
## Схема для управления доступом:
### User:
- Id
- Email
- First_name
- Last_name
- Middle_name

### Group(Role):
- Id
- Name

### User Group:
- Id 
- User_id (FK)
- Group_id (FK)

### Permission:
- Id
- Codename (например, add_psot, change_post)   
- Name

### Group Permission:
- Id
- Group_id (FK)
- Permission_id (FK)

**Permission:** Создаются атомарные действия, например: add_post, change_post, delete_post.

**Group:** Создаются роли, например: «Manager» и «User».

**Group Permission:** Настраиваются связи. Роли «Редактор» назначаются все три права, а «User» — только add_post и view_post.

Когда в системе регистрируется новый человек (таблица User), добавляется запись в связующую таблицу (User Group).


import pprint
import praw
from datetime import datetime
from peewee import *

db = SqliteDatabase("my_database.db")


class BaseModel(Model):
    class Meta:
        database = db


class SavedEntity(BaseModel):
    reddit_id = CharField()
    title = CharField()
    type = CharField()
    subreddit = CharField(index=True)
    date = DateTimeField(default=datetime.now)
    permalink = CharField()
    text = TextField()


class Tag(BaseModel):
    val = CharField()


class EntityTag(BaseModel):
    entity = ForeignKeyField(SavedEntity)
    tag = ForeignKeyField(Tag)

    class Meta:
        primary_key = CompositeKey("entity", "tag")


reddit = praw.Reddit("bot1", user_agent="organizer by /u/jbrr25 0.1")

""" submission = reddit.submission(id='39zje0')
print(submission.title) # to make it non-lazy
pprint.pprint(vars(submission))

comment = reddit.comment(id='cthwcdf')
print(comment.body) # to make it non-lazy
pprint.pprint(vars(comment)) """


def save_to_sql():
    ls = []
    db.connect()
    db.get_tables()
    db.create_tables([SavedEntity, Tag, EntityTag])
    self_tag = Tag.create(val="self")
    link_tag = Tag.create(val="link")
    for s in reddit.user.me().saved(limit=10):
        # print("------------------")
        if isinstance(s, praw.models.Submission):
            # print("Post from {}".format(s.subreddit_name_prefixed))
            # print(s.title)
            its = SavedEntity(
                title=s.title,
                reddit_id=s.id,
                type="post",
                subreddit=s.subreddit_name_prefixed,
                date=datetime.fromtimestamp(s.created),
                permalink=s.permalink,
            )
            item_to_print = {
                "title": s.title,
                "type": "post",
                "subreddit": s.subreddit_name_prefixed,
                "date": datetime.fromtimestamp(s.created),
                "permalink": s.permalink,
                "tags": [],
            }
            if s.is_self:
                its.text = s.selftext
                its.save()
                EntityTag.create(entity=its, tag=self_tag)
                item_to_print["text"] = s.selftext
                # print(s.selftext)
            else:
                its.text = s.url
                its.save()
                EntityTag.create(entity=its, tag=link_tag)
                item_to_print["text"] = s.url
                # print(s.url)
            ls.append(item_to_print)
        else:
            SavedEntity.create(
                title=s.submission.title,
                reddit_id=s.id,
                type="comment",
                subreddit=s.subreddit_name_prefixed,
                date=datetime.fromtimestamp(s.created),
                permalink=s.permalink,
                text=s.body,
            )

            item_to_print = {
                "title": s.submission.title,
                "type": "comment",
                "subreddit": s.subreddit_name_prefixed,
                "date": datetime.fromtimestamp(s.created),
                "permalink": s.permalink,
                "tags": [],
                "text": s.body,
            }
            ls.append(item_to_print)
            # print("Comment in thread '{}' from {}".format(s.submission.title,
            #                                              s.subreddit_name_prefixed))
            # print(s.body)
    db.close()
    pprint.pprint(ls)


def assing_tag(entity):
    programming = [
        "r/programming",
        "r/learnprogramming",
        "r/Python",
        "r/java",
        "r/javascript",
        "r/learnpython",
        "r/csharp",
        "r/dotnet",
        "r/unity3d",
        "r/rust",
        "r/Kotlin",
        "r/ruby",
        "r/webdev",
        "r/MachineLearning",
        "r/androiddev",
    ]
    programming_tag = Tag.create(val="programming")

    resources = [
        "r/wallpapers",
        "r/Android",
        "r/web_design",
        "r/unixporn",
        "r/skyrim",
        "r/technology",
        "r/tasker",
        "r/pcmasterrace",
        "r/movies",
        "r/mexico",
        "r/linuxmint",
        "r/linux",
    ]
    resources_tag = Tag.create(val="resources")

    knowledge = ["csharp", "programming"]
    knowledge_tag = Tag.create(val="knowledge")

    if entity.subreddit in programming:
        EntityTag.create(entity=entity, tag=programming_tag)

    if entity.subreddit in resources:
        EntityTag.create(entity=entity, tag=resources_tag)

    if entity.subreddit in knowledge:
        EntityTag.create(entity=entity, tag=knowledge_tag)


save_to_sql()

import pprint
import praw
from datetime import datetime
from peewee import *

db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class SavedEntity(BaseModel):
    redditId = CharField()
    title = CharField()
    type = CharField()
    subreddit = CharField()
    date = DateTimeField(default= datetime.now)
    permalink = CharField()
    val = TextField()

class Tag(BaseModel):
    entity = ForeignKeyField(SavedEntity, backref='tags')
    val = CharField()

reddit = praw.Reddit('bot1', user_agent='organizer by /u/jbrr25 0.1')

''' submission = reddit.submission(id='39zje0')
print(submission.title) # to make it non-lazy
pprint.pprint(vars(submission))

comment = reddit.comment(id='cthwcdf')
print(comment.body) # to make it non-lazy
pprint.pprint(vars(comment)) '''
def saveToSql():
    ls = []
    db.connect()
    db.create_tables([SavedEntity, Tag])
    for s in reddit.user.me().saved(limit=None):
        #print("------------------")
        if isinstance(s, praw.models.reddit.submission.Submission):
            #print("Post from {}".format(s.subreddit_name_prefixed))
            #print(s.title)
            its = SavedEntity(title=s.title, redditId=s.id, type='post', subreddit=s.subreddit_name_prefixed, date=datetime.fromtimestamp(s.created), permalink=s.permalink)
            item = {'title': s.title, 'type': "post", 'subreddit': s.subreddit_name_prefixed, 'date': datetime.fromtimestamp(s.created), 'permalink': s.permalink, 'tags': []}
            if s.is_self:
                its.val = s.selftext
                its.save()
                Tag.create(entity=its, val='self')
                item["val"] = s.selftext
                item['tags'].append("self")
                #print(s.selftext)
            else:
                its.val = s.url
                its.save()
                Tag.create(entity=its, val='link')
                item["val"] = s.url
                item['tags'].append("link")
                #print(s.url)
            ls.append(item)
        else:
            its = SavedEntity.create(title=s.submission.title, redditId=s.id, type='comment', subreddit=s.subreddit_name_prefixed, date=datetime.fromtimestamp(s.created), permalink=s.permalink, val=s.body)
            item = {'title': s.submission.title, 'type': "comment", 'subreddit': s.subreddit_name_prefixed, 'date': datetime.fromtimestamp(s.created), 'permalink': s.permalink, 'tags': []}
            item['val'] = s.body
            ls.append(item)
            #print("Comment in thread '{}' from {}".format(s.submission.title,
            #                                              s.subreddit_name_prefixed))
            #print(s.body)

    pprint.pprint(ls)

saveToSql()
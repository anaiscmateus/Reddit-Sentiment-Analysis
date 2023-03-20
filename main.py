import openai
import praw
import os

reddit = praw.Reddit(client_id=os.environ.get('reddit_client_id'),
                     client_secret=os.environ.get('reddit_client_secret'),
                     user_agent ='sentiment analysis test'
                     )

def get_titles_and_comments(subreddit="stocks", limit=6, num_comments=3, skip_first=2):
    subreddit = reddit.subreddit(subreddit)
    title_and_comments = {}

    for counter, post in enumerate(subreddit.hot(limit=limit)):

        if counter < skip_first:
            continue
        counter += (1-skip_first)

        title_and_comments[counter] = ""
        submission = reddit.submission(post.id)
        title = post.title

        title_and_comments[counter] += 'Title: '+title+"\n\n"
        title_and_comments[counter] += "Comments: \n\n"

        comment_counter = 0
        for comment in submission.comments:
            if not comment.body == "[deleted]":
                title_and_comments[counter] += comment.body+"\n"
                comment_counter += 1
            if comment_counter == num_comments:
                break
    return title_and_comments

titles_and_comments = get_titles_and_comments()

def create_prompt(title_and_comments):
    task = "Return the stock ticker or company name mentioned in the following title and comments and classify the sentiment around the company as positive, negative, or neutral. If no ticker or company is mentioned write 'No Company mentioned'\n\n"
    return task + title_and_comments

for key, title_with_comments in titles_and_comments.items():
    prompt = create_prompt(title_with_comments)

    response = openai.Completion.create(engine='text-davinci-003',
                                        prompt=prompt,
                                        max_tokens=256,
                                        temperature=0,
                                        top_p=1.0
                                        )
    print(title_with_comments)
    print(f"Sentiment Report from OpenAI: {response['choices'][0]['text']}")
    print('--------------------')
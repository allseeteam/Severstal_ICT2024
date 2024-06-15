from search import ask_yagpt, make_prompt_by_html
from youtube_transcript_api import YouTubeTranscriptApi
from youtubesearchpython import VideosSearch


def video_inference(query, api_key, model_id):
    video = find_youtube_video(query)
    video_id = video['id']
    video_url = video['url']
    video_title = video['title']
    print(f'Лучшее видео по запросу: {video_url}')
    transcription = get_video_transcription(video_id)
    summarization = ask_yagpt(make_prompt_by_html(
        transcription), api_key, model_id)
    return {
        'url': video_url,
        'text': summarization,
        'title': video_title,
        'raw_transcription': transcription
    }


def get_video_transcription(video_id):
    transcribe = YouTubeTranscriptApi.get_transcript(
        video_id, languages=('ru',))
    total_len = 0
    i = 0
    lines = []
    while total_len < 5000 and i < len(transcribe):
        # нарезаем, чтобы поместилось в модельку
        # хорошо бы сохранять в базу полностью, но успеваем
        text = transcribe[i]['text']
        lines.append(text)
        total_len += len(text)
        i += 1

    transcribe = ' '.join(lines)
    return transcribe


def find_youtube_video(query):
    videosSearch = VideosSearch(query, limit=1)
    try:
        return videosSearch.result()['result'][0]
    except Exception as e:
        print(e)
    return None

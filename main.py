# main.py
# AutoContentGen - Initial version of an AI-driven content generation tool
# AutoContentGen - AI驱动内容生成工具的初始版本
# This is the first release; developers are invited to improve or extend it via GitHub!
# 这是首个版本，欢迎开发者通过 GitHub 改进或扩展！

import schedule
import time
import os
from trend_analysis import get_trend_scores
from prompt_generation import generate_prompts
from image_generation import generate_image
from video_generation import generate_video
from video_upscaling import upscale_video
from ai_decision import select_best_result

# Configuration / 配置
DOMAIN = "Artificial Intelligence"
SUBTOPICS = ["Machine Learning", "Natural Language Processing", "Robotics"]
TREND_THRESHOLD = 50
NUM_PROMPTS = 5
NUM_TO_SELECT = 2
PUBLISH_PLATFORM = "Social Media"

# Directories / 目录
DATA_DIR = 'data'
PROMPTS_DIR = os.path.join(DATA_DIR, 'prompts')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
VIDEOS_DIR = os.path.join(DATA_DIR, 'videos')
UPSCALED_DIR = os.path.join(DATA_DIR, 'upscaled_videos')

for dir_path in [DATA_DIR, PROMPTS_DIR, IMAGES_DIR, VIDEOS_DIR, UPSCALED_DIR]:
    os.makedirs(dir_path, exist_ok=True)

def run_pipeline():
    print("Starting automated pipeline... / 开始自动化流程...")

    # Step 1: Trend analysis from multiple APIs / 从多个 API 获取趋势分析
    trend_data_openai = get_trend_scores(SUBTOPICS, api="openai")
    trend_data_baidu = get_trend_scores(SUBTOPICS, api="baidu")
    combined_trend_data = {k: max(trend_data_openai.get(k, 0), trend_data_baidu.get(k, 0)) for k in set(trend_data_openai) | set(trend_data_baidu)}
    hot_subtopics = [subtopic for subtopic, score in combined_trend_data.items() if score > TREND_THRESHOLD]

    if not hot_subtopics:
        print("No hot subtopics found. / 未找到热门子主题。")
        return

    # AI decision: Select best subtopic / AI 决策：选择最佳子主题
    selected_subtopic = select_best_result(
        hot_subtopics,
        "Choose the most relevant subtopic for content generation / 选择最适合内容生成的子主题",
        num_to_select=1
    )[0]
    print(f"Selected subtopic: {selected_subtopic} / 选择的子主题: {selected_subtopic}")

    # Step 2: Generate prompts from multiple APIs / 从多个 API 生成提示词
    prompts_openai = generate_prompts(selected_subtopic, api="openai")
    prompts_baidu = generate_prompts(selected_subtopic, api="baidu")
    all_prompts = prompts_openai + prompts_baidu

    # AI decision: Select best prompts / AI 决策：选择最佳提示词
    selected_prompts = select_best_result(
        all_prompts,
        "Choose the most creative and descriptive prompts / 选择最具创意和描述性的提示词",
        num_to_select=NUM_TO_SELECT
    )
    print(f"Selected prompts: {selected_prompts} / 选择的提示词: {selected_prompts}")

    # Step 3: Generate images from multiple APIs / 从多个 API 生成图像
    image_paths = []
    for prompt in selected_prompts:
        image_path_sd = generate_image(prompt, IMAGES_DIR, api="stable_diffusion")
        image_path_baidu = generate_image(prompt, IMAGES_DIR, api="baidu")
        if image_path_sd:
            image_paths.append(image_path_sd)
        if image_path_baidu:
            image_paths.append(image_path_baidu)

    # AI decision: Select best images / AI 决策：选择最佳图像
    selected_images = select_best_result(
        image_paths,
        "Choose the highest quality and most relevant images / 选择最高质量且最相关的图像",
        num_to_select=NUM_TO_SELECT
    )
    print(f"Selected images: {selected_images} / 选择的图像: {selected_images}")

    # Step 4: Generate videos from multiple APIs / 从多个 API 生成视频
    video_paths = []
    for image_path in selected_images:
        video_path_runway = generate_video(image_path, VIDEOS_DIR, api="runwayml")
        video_path_baidu = generate_video(image_path, VIDEOS_DIR, api="baidu")
        if video_path_runway:
            video_paths.append(video_path_runway)
        if video_path_baidu:
            video_paths.append(video_path_baidu)

    # AI decision: Select best videos / AI 决策：选择最佳视频
    selected_videos = select_best_result(
        video_paths,
        "Choose the most engaging and high-quality videos / 选择最具吸引力和高质量的视频",
        num_to_select=NUM_TO_SELECT
    )
    print(f"Selected videos: {selected_videos} / 选择的视频: {selected_videos}")

    # Step 5: Upscale videos from multiple APIs / 从多个 API 增强视频
    upscaled_paths = []
    for video_path in selected_videos:
        upscaled_path_topaz = upscale_video(video_path, UPSCALED_DIR, api="topaz")
        upscaled_path_baidu = upscale_video(video_path, UPSCALED_DIR, api="baidu")
        if upscaled_path_topaz:
            upscaled_paths.append(upscaled_path_topaz)
        if upscaled_path_baidu:
            upscaled_paths.append(upscaled_path_baidu)

    # AI decision: Select best upscaled video for publishing / AI 决策：选择最佳增强视频用于发布
    final_video = select_best_result(
        upscaled_paths,
        "Choose the best video for publishing based on quality and relevance / 根据质量和相关性选择最佳发布视频",
        num_to_select=1
    )[0]
    print(f"Final video for publishing: {final_video} / 最终发布视频: {final_video}")

    # Step 6: Publish or store / 发布或存储
    if PUBLISH_PLATFORM == "Social Media":
        print(f"Publishing to social media: {final_video} / 发布到社交媒体: {final_video}")
        # Add publishing logic here / 在此添加发布逻辑
    else:
        print(f"Storing to storage space: {final_video} / 存储到存储空间: {final_video}")
        # Add storage logic here / 在此添加存储逻辑

# Schedule daily run at 8 AM / 每天早上 8 点运行
schedule.every().day.at("08:00").do(run_pipeline)

print("Starting scheduler, running daily at 8 AM... / 启动调度器，每天早上 8 点运行...")
while True:
    schedule.run_pending()
    time.sleep(60)

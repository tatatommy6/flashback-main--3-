import os
import time
import dotenv
from runwayml import RunwayML

# .env 파일에서 환경 변수 불러오기
dotenv.load_dotenv()

# API 키 불러오기
client = RunwayML(api_key=os.getenv('RUNWAY_API_SECRET'))

# 이미지에서 비디오 생성 작업
image_to_video = client.image_to_video.create(
    model="gen3a_turbo",
    prompt_image="https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
    prompt_text="a cute cat",
)

# 생성된 영상의 ID
job_id = image_to_video.id
print(f"{job_id}")

# 작업 상태 확인 및 백오프 전략 적용


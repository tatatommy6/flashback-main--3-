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
    prompt_text="a man standing on a mountain",
)

# 생성된 영상의 ID
job_id = image_to_video.id
print(f"생성된 작업 ID: {job_id}")

# 작업 상태 확인 및 백오프 전략 적용
max_retries = 5  # 최대 재시도 횟수
retry_delay = 10  # 재시도 간격(초)
retry_count = 0

while retry_count < max_retries:
    try:
        # 작업 상태 확인
        job_status = client.jobs.get(job_id)

        if job_status['status'] == 'succeeded':
            # 작업이 성공하면 결과물 다운로드
            result = client.jobs.download(job_id)

            # 다운로드할 파일 경로 지정
            output_path = "C:/Users/tatat/Downloads/generated_video.mp4"

            # 결과물을 파일로 저장
            with open(output_path, "wb") as f:
                f.write(result.content)

            print(f"영상이 {output_path}에 저장되었습니다.")
            break

        elif job_status['status'] == 'failed':
            print("작업이 실패했습니다.")
            break

        else:
            print(f"작업 상태: {job_status['status']}. 작업이 완료될 때까지 대기 중...")

    except Exception as e:
        print(f"에러 발생: {e}. {retry_delay}초 후에 다시 시도합니다...")
        retry_count += 1
        time.sleep(retry_delay)

if retry_count == max_retries:
    print("최대 재시도 횟수를 초과했습니다. 나중에 다시 시도해 보세요.")

from utils import before_putDB, putting_prompt_DB, putting_video_DB, search_prompt_API, search_video_API
from utils.log import Logger
logger = Logger(__file__)

def putDB(
        
        prompt_file_path: str,
        video_file_path: str,
        model_file: str,
        id: str,
        pw: str,
        prompt_index: str,
        video_index: str,
        device: str,
    ):
        """
        elastic DB에 데이터를 넣는 작업을 진행한다. prompt와 image에 대한 vector data를 넣는다.

        Args:
            prompt_file_path (str): prompt에 대한 yaml파일 경로
            video_file_path (str): video에 대한 dir path
            model_file (str): model file 경로
            id (str): elasticsearch id
            pw (str): elasticsearch pw
            prompt_index (str): elasticsearch에 저장될 prompt index 지정
            video_index (str): elasticsearch에 저장될 video index 지정
            device (str):  "cpu", "mps", "cuda" 중에 하나

        """

        def inner(
            prompt_file_path, video_file_path, model_file, id, pw, prompt_index, video_index, device
        ):
            """putDB 함수의 inner를 정의한다."""
            client, df, video_data, model, id, pw = before_putDB(
                prompt_file_path=prompt_file_path,
                video_file_path=video_file_path,
                model_file=model_file,
                id=id,
                pw=pw,
                prompt_index=prompt_index,
                video_index=video_index,
                device=device,
            )

            putting_prompt_DB(client, df, model, prompt_index)
            putting_video_DB(client, video_data, model, video_index)
            search_prompt_API(client)
            search_video_API(client)

        inner(
            prompt_file_path, video_file_path, model_file, id, pw, prompt_index, video_index, device
        )
        logger.info("데이터베이스 작업이 모두 끝났습니다.")
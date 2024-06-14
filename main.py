from utils.putDB import putDB

putDB(
    prompt_file_path="cfg/prompt_for_vector.yaml",
    video_file_path="asset/fire.mp4",
    model_file="model/c4_vit32_vtt_b128_ep5.pth",
    id="your_id",
    pw="pw",
    prompt_index="prompt_index",
    video_index="video_index",
    device="mps",
)
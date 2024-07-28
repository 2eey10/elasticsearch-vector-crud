import cv2
import numpy as np


def _calc_tile_cnt(origin_size, tile_size, margin_size):
    tile_cnt = (origin_size - margin_size) / (tile_size - margin_size)
    return int(tile_cnt)


def _make_tiled_images(tile_size, frame: np.array, margin_min=0.25):
    h, w = frame.shape[:2]
    margin_size = int(tile_size * margin_min)
    margin_minus_tile_size = tile_size - margin_size

    # Initializing
    return_frames = []

    # Available test
    if margin_minus_tile_size * 2 >= h and margin_minus_tile_size * 2 >= w:
        return [frame], 1, 1

    # Count calculatable tile
    x_tile_cnt = _calc_tile_cnt(w, tile_size=tile_size, margin_size=margin_size)
    y_tile_cnt = _calc_tile_cnt(h, tile_size=tile_size, margin_size=margin_size)
    end_x_coord = tile_size
    start_x_coord = 0
    y_tile_start_end_coord = []
    for _x in range(x_tile_cnt):
        end_y_coord = tile_size
        start_y_coord = 0
        for _y in range(y_tile_cnt):
            if _x == 0:
                y_tile_start_end_coord.append([start_y_coord, end_y_coord])
            tile = frame[start_y_coord:end_y_coord, start_x_coord:end_x_coord]
            return_frames.append(tile)

            start_y_coord = end_y_coord - margin_size
            end_y_coord = end_y_coord - margin_size + tile_size
        tile = frame[-tile_size:, start_x_coord:end_x_coord]
        return_frames.append(tile)

        start_x_coord = end_x_coord - margin_size
        end_x_coord = end_x_coord - margin_size + tile_size

    for start_y_coord, end_y_coord in y_tile_start_end_coord:
        tile = frame[start_y_coord:end_y_coord, -tile_size:]
        return_frames.append(tile)

    tile = frame[-tile_size:, -tile_size:]
    return_frames.append(tile)

    x_tile_cnt += 1
    y_tile_cnt += 1

    # add original frame
    return_frames.append(frame)
    return return_frames, x_tile_cnt, y_tile_cnt


def preprocess_input_image(model, origin_image, tile_size, margin_size):
    # tiling
    tiles, wn, hn = _make_tiled_images(
        tile_size=tile_size, frame=origin_image, margin_min=margin_size
    )
    # resize
    tiles = np.array(model.process_video(tiles, size=224))
    return tiles, wn, hn


def combine_image_tiles(tiles, wn, hn):
    tiles_view = np.transpose(tiles, (0, 2, 3, 1))
    h, w = tiles_view.shape[1:3]

    t_min = np.min(tiles_view)
    t_max = np.max(tiles_view)
    tiles_view = ((tiles_view - t_min) / (t_max - t_min) * 255).astype(np.uint8)
    tiles_comb = np.hstack(
        [np.vstack([tiles_view[i * hn + j] for j in range(hn)]) for i in range(wn)]
    )

    # make grid
    tiles_comb[[j for j in range(0, tiles_comb.shape[0], h)] + [-1], :] = [0, 255, 255]
    tiles_comb[:, [i for i in range(0, tiles_comb.shape[1], w)] + [-1]] = [0, 255, 255]
    return tiles_comb


def get_frame(video_path):
    video = cv2.VideoCapture(video_path)
    success, image = video.read()
    video.release()  # 자원을 바로 해제
    if success:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    else:
        return None

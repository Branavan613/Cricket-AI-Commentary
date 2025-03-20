def in_box(point, box):
    x, y = point
    x_min, x_max, y_min, y_max = box
    return x_min <= x <= x_max and y_min <= y <= y_max

def get_midpoint(box):
    x_min, x_max, y_min, y_max = box
    return [(x_min + x_max) / 2, (y_min + y_max) / 2]
def process(data, frame_height, frame_width):
    pitch = False
    batters = data["batsman"] if data["batsman"] else []
    balls = data["ball"] if data["ball"] else []
    batter = False
    batters_box = [frame_width * 0.35, frame_width * 0.65 , frame_height * 0.05, frame_height * 0.5]

    for batter in batters:
        if in_box(get_midpoint(batter["position"]), batters_box):
            batters_box = [batter["position"][0] * 0.8, batter["position"][1] * 1.15, batter["position"][2] * 0.95, batter["position"][3] * 1.15]
            batter = True
            break
    if batter:
        for ball in balls:
            if in_box(get_midpoint(ball["position"]), batters_box):
                pitch = True
                break
    return pitch
            
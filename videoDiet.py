import ffmpeg
import argparse
import os

# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser()
# 입력받을 인자값 등록
parser.add_argument('--target', required=True, help='target video path')
# 입력받은 인자값을 args에 저장 (type: namespace)
args = parser.parse_args()

# ffmpeg으로 변환할 때는 기존 파일에 덮어쓰기가 안 되므로 변환된 파일들을 저장할 폴더를 생성한다
os.mkdir("resized")

# 폴더 내의 파일 목록을 모두 가져온다
files = os.listdir(args.target)

# 파일 목록 중에 mp4 파일만 추린다
mp4s = [file for file in files if file[-3:] == "mp4"]

# 변환 중 에러가 발생하는 경우가 있어 에러 처리를 위한 리스트를 만든다
err = []

# 파일 변환을 시도한다(try) 에러가 날 경우 변환 중이던 파일을 지우고 파일명을 err리스트에 추가한다.(except)
for mp4 in mp4s:
    try:
        ffmpeg.input(mp4).output("resized/"+mp4, crf=23, vsync="vfr").run()
    except:
        os.remove("resized/"+mp4)
        err.append(mp4)

# 파일이 resized 폴더 내에 있다면(에러가 나지 않고 변환되어 옮겨져 있다면) 원래 폴더에서 파일을 삭제한다
# if mp4 in os.listdir("resized"):
#     os.remove(mp4)

# mp4 파일 목록을 순회하면서 오류 났던 파일(err 리스트)을 제외한 나머지 파일을 원래 폴더로 모두 옮긴다
# for mp4 in mp4s:
#     if mp4 in err:
#         pass
#     else:
#         os.replace("resized/"+mp4, mp4)

# resized 폴더를 삭제한다
# os.rmdir("resized")

# 변환에 실패한 파일 목록을 출력한다
print("실패한 목록: \n", err)
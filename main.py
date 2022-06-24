from ast import While
from inspect import currentframe
from tkinter import W
import numpy as np
from torch import ge
import cv2
import time


def get_video_props(video_fname="shorts_video.mp4"):
    cap = cv2.VideoCapture(video_fname)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcc = cap.get(cv2.CAP_PROP_FOURCC) #h264=x264, vp9=fmp4
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    OPACITY = int(cap.get(cv2.COLOR_BGRA2RGBA))
    print('----\n--\n--\n--\n--\n----')

    while cap.isOpened():
        r, f = cap.read(cv2.IMREAD_UNCHANGED)
        # print(r) # true
        print(np.shape(f))
        break


    duration = frame_count/fps
    
    if '-' in video_fname:
        
        print("Opacity (alpha) : ", OPACITY)
        print("codec (fcc) : ",fcc) #fcc,fps, w,h
        print("frame_count : " , frame_count)
        print("scale (wxh) : ", w , 'x', h)
        print("duration : ", duration)
        import os
        file_size = os.path.getsize(video_fname)
        print("FileSize :", file_size/1000**2, "Mbytes")

        log = {"size(MB)" : file_size/1000**2,
        "duration(s)" : round(duration,4),
        'frame_count' : frame_count,
        'scale (wxh)' : "".join([str(w),'x',str(h)]),
        'opacity' : OPACITY
        }

        write_logging(video_fname, str(log))

    return h , duration, fps

def change_video(filename="shorts_video.mp4", 
                    _fps = 30, 
                    _scale = 1080, 
                    # _speed = 1.0,
                    # _end = 160,
                    _fmt ='yuv420p',
                    _replica = 1
                     ):
    
    '''
    resolution
    scale=640x480
    scale=800x480
    scale=1280x720
    scale=1920x1080 
    '''
    import ffmpeg


    input = ffmpeg.input(filename)
    # a = ffmpeg.concat(input, input)
    # input = ffmpeg.concat(*[input for i in range(_replica)])

    video = input.video.filter('fps', fps=_fps, round='up')\
            .filter('scale', -1, _scale)
    audio = input.audio

    # end_frame = _fps*i_seconds
    # video = video1.trim(start=0, end=end_frame)\
    #         .setpts('PTS-STARTPTS')

    # audio = input.audio.filter_('atrim',start=0, end=end_frame)\
    #         .filter('asetpts','PTS-STARTPTS')

    # it plays the last image at the last period alone...
    # video = video.setpts(f'{ str(_speed) }*PTS')

    
    name = filename.replace('./data/','')
    name = name.split('.')[0]
    output_filename = f'{name}-fps{_fps}-rsl{_scale}-{_fmt}-rep{_replica}'
    output_filename += '.mp4' if _fmt[-1] != 'a' else '.webm' 
    
    out_path = './output/' + output_filename
    org_out_path = out_path.replace(f"-rep{_replica}","")

    # joined = ffmpeg.concat(video,audio,v=1,a=1)
    # out = ffmpeg.output(joined[0], joined[1],out_path
    
    out = ffmpeg.output(video,audio, org_out_path
        , pix_fmt = _fmt ).run(overwrite_output=True) #pix_fmt = yuv420p, rgba/bgra
        # format table -> https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=wingjyn&logNo=220269909291
    
    #ffmpeg
    import os
    # replicas = "|".join([output_filename for i in range(_replica)])
    # command = f'ffmpeg -i "concat:{replicas}" -c copy {output_filename}' 
    command = f'ffmpeg -y -stream_loop {_replica} -i {org_out_path} -c copy {out_path}' 
    print(command)
    os.system(command)
    

    return out_path


import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='/home/bens/Downloads/aug-image-data/log/app.log',
                filemode='w')
# create logger with 'job token or filename'
logger1 = logging.getLogger('init.phase')
logger2 = logging.getLogger('produce.phase')
logger3 = logging.getLogger('consume.phase')
logger4 = logging.getLogger('final.phase')


def write_logging(job_name,txt):
    log = ' | '.join([job_name,txt])
    logger1.info(log)



if __name__ == "__main__":


    # ffmpeg -i path/to/filename
    # stream : codec, format, resolution
    
    # fps, scale(resolution), rep, fmt
    fps_list = [i for i in range(16,60,4)] #11
    h_scale_list = [480,640,800,1080] #4 480-1080
    # replica_list = [i for i in range(2,6)] # 5(6)


    #i_replica
    params_list = [(i_fps, i_h_scale, 2 ) 
    #   for i_replica in replica_list
        for i_h_scale in h_scale_list 
          for i_fps in fps_list
       ]

    import glob 

    try:
        for i_file in glob.glob('./data/*') :
            
            for i_params in params_list :
                # print(i_params)

                out_path = change_video(filename=i_file, 
                                _fps = i_params[0], 
                                _scale = i_params[1], 
                                # _speed = 2,
                                # _end = 10000,
                                _fmt ='yuv420p',
                                _replica = i_params[2])
                
                break
    except Exception as err :
        logger1.error(err)
        

    # import os
    # import glob 
    # for i_file in glob.glob('./data/*') :
    #     get_opacity(i_file)

    # get video info

def manipulate_fps(video_fname="shorts_video.mp4", value=16):
    cap = cv2.VideoCapture(video_fname)
    cap.set(cv2.CAP_PROP_FPS, value)
    # get_video_props()

def amplify():
    fcc = cv2.VideoWriter_fourcc(*'')
    return

def split_video_save_image(video_fname="shorts_video.mp4"):
    cap = cv2.VideoCapture(video_fname)
    currentframe = 0

    while(True):  
        # reading from frame
        ret,frame = cap.read()
    
        if ret and (currentframe < 10):
            # if video is still left continue creating images
            name = './data/frame' + str(currentframe) + '.png'
            print ('Creating...' + name)

            # img read 
            # cv2.imread(path,cv2.IMREAD_UNCHANGED) # rgba
    
            # writing the extracted images
            cv2.imwrite(name, frame)
    
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

def get_opacity(filename): #'./data/frame1.png'
    from PIL import Image
    img = Image.open(filename)
    img = img.convert("RGBA")
    datas = img.getdata()
    opacity = [ p[-1] for p in datas]
    arr = np.array(opacity)
    # measures of central tendency
    mean = np.mean(arr)
    median = np.median(arr)
    
    # measures of dispersion
    min = np.amin(arr)
    max = np.amax(arr)
    range = np.ptp(arr)
    variance = np.var(arr)
    sd = np.std(arr)
    
    # print("Descriptive analysis")
    # print("Array =", arr)
    # print("Measures of Central Tendency")
    print("Mean =", mean)
    # print("Median =", median)
    # print("Measures of Dispersion")
    # print("Minimum =", min)
    # print("Maximum =", max)
    # print("Range =", range)
    # print("Variance =", variance)
    print("Standard Deviation =", sd)
    # print("cv : " ,mean/sd)
    return mean

def save_video(filename, cap, fcc, fps, width, height):
#     path = './changed'
#     # cv2.VideoWriter(저장 위치, 코덱, 프레임, (가로, 세로))
#     out = cv2.VideoWriter(f'{path}/{filename}.mp4', fcc, fps, (width, height))
    
#     while True:
#         ret, frame = cap.read()
#         # cv2.imshow('none', frame) # 촬영되는 영상보여준다.
#         # 촬영되는 영상을 저장하는 객체에 써준다.
# 	    out.write(frame) 
#         k = cv2.waitKey(1) & 0xff
#         if k == 27:
#             break
#     # cap 객체 해제
#     cap.release()
#     # out 객체 해제
#     out.release()
#     cv2.destroyAllWindows()
    return



def trim_video(filename="shorts_video.mp4"):
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
    
    h, duration = get_video_props(filename)
    print(duration)
    ext = filename.split('.')[-1]
    name = "."+filename.split('.')[-2]

    print(ext, name)



    for i_seconds in range(5,60,5): # 0s ~60s
        if i_seconds > duration :
            print('=======\n=======\n=======\n=======\n')
            print(filename)
            print(i_seconds)
            break
        
        # i_seconds = str(i_seconds)
        new_filename = name+str(i_seconds).zfill(2)+"."+ext

        ffmpeg_extract_subclip(
            filename,
            0,
            i_seconds,
            new_filename
        )

        # command = f"ffmpeg -i {filename} -ss 00:00:01 -to 00:00:{str(i_seconds)} -c:v copy -c:a copy {new_filename}"
        # print(command)

        # import os
        # os.system('cd output')
        # os.system(command)

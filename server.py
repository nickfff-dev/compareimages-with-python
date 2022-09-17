from flask import Flask, Response, request, abort, render_template_string, send_from_directory,jsonify,redirect
from threading import Thread
import os
import random





app = Flask(__name__)




# function to select 2 random images from any two different subfolders save the selected to selectedimages.text

def selectimages():

    MainFolder = os.path.join( 'static', 'images')

    subfolders = [f.path for f in os.scandir(MainFolder) if f.is_dir() ]
    twoimages = []
    imagenames = []
    with open('selectedimages.txt', 'r') as f: 
        selectedimages = f.read().splitlines()
        for image in selectedimages:
            imagename = image.split('/')[-1]
            imagenames.append(imagename)
    while True:
        randomfolder = random.choice(subfolders)
        randomimage1 =  os.path.join(randomfolder, random.choice(os.listdir(randomfolder)))
        if randomimage1 not in imagenames:
            print("random", randomimage1)
            twoimages.append(randomimage1)
            imagenames.append(randomimage1)
            break
    while True:
        randomfolder = random.choice(subfolders)
        randomimage2 =  os.path.join(randomfolder, random.choice(os.listdir(randomfolder)))
        if randomimage2 not in imagenames:
            print("random", randomimage2)
            twoimages.append(randomimage2)
            imagenames.append(randomimage2)
            break
    return twoimages










@app.route("/background_process_test/")
def background_process_test():
    imgname = request.args.get('imagepath', 0, type=str)
    print(request.args)
    with open('selectedimages.txt', 'r') as f:
        selectedimages = f.read().splitlines()
        if imgname not in selectedimages:
            with open('selectedimages.txt', 'a') as f:
                f.write(imgname + '\n')
        else:   
            print('image already selected cannot be added to li')
    # refresh the page to show the new image
    return ("nothing")


    

@app.route('/')
def index():
    twotandomimages = selectimages()


    print(twotandomimages)

    # show two images side by side

    return render_template_string(''' 
    

    <html>

    <head>

    <style>

    .column {

       display: flex;

       flex-direction: row;

       justify-content: center

    }

    h1{

        text-align: center;

    }

    img{

        margin-inline: 30px;

        border: 2px solid #000

    }

    </style>

    </head>

    <body>

    <h1>Image Comparison</h1>

    <div class="column">

    <img id="{{twotandomimages[0]}}" src="{{twotandomimages[0]}}" alt="Snow"  width=512 height=512>
  
  

    <img id="{{twotandomimages[0]}}"src="{{twotandomimages[1]}}" alt="Forest" width=512 height=512 >

    </div>
 <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"> </script>
<script type="text/javascript">
$(function() {
    $('img').click(function(event) {
        var imagepath = $(this).attr('id');
        $.ajax({
            url: '/background_process_test/',
            data: {
                'imagepath': imagepath},
            type: 'GET',
        }).done(function(data) {
                window.location.replace("/");
        });
    });


     })
     </script>
    </body>

    </html>

    ''', twotandomimages=twotandomimages)
    
    
   

    








if __name__ == '__main__':


    Thread(target=app.run(host= '127.0.0.1', port= "8000", debug=True)).start()
    
   



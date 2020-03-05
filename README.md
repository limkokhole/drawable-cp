# drawable-cp
Copy drawable icons obtained from designer to Android Studio project

#### Usage 1 ([1] Already navigate to ~/Downloads/my_icons, so no need -d [2] -pd &lt;android studio project root path&gt; [3] --debug means only print log without perform copy action):

    xb@dnxb:~/Downloads/my_icons$ python3 ~/Downloads/misc/python/drawable_cp.py -pd ~/AndroidStudioProjects/hello-world/ --debug
    proj_dir: /home/xiaobai/AndroidStudioProjects/hello-world/app/src/main/res/ 

    From /home/xiaobai/Downloads/my_icons/2/xxxhdpi/cool.png
    To: /home/xiaobai/AndroidStudioProjects/hello-world/app/src/main/res/drawable-xxxhdpi 

    From /home/xiaobai/Downloads/my_icons/2/hdpi/cool.png
    To: /home/xiaobai/AndroidStudioProjects/hello-world/app/src/main/res/drawable-hdpi 

    From /home/xiaobai/Downloads/my_icons/2/xxhdpi/cool.png
    To: /home/xiaobai/AndroidStudioProjects/hello-world/app/src/main/res/drawable-xxhdpi

    ...

#### Usage 2 ([1] -d &lt;icons of designer path&gt;, [2] --prefix-designer &lt;Extra prefix of folder name&gt; ):

    xb@dnxb:~/Downloads/misc/python/drawable-cp$ python3 ~/Downloads/misc/python/drawable-cp/drawable_cp.py -pd ~/AndroidStudioProjects/hello-world/ --debug -d ~/Downloads/my_icons/  --prefix-designer pika- 
    proj_dir: /home/xiaobai/AndroidStudioProjects/hello-world/app/src/main/res/ 

    From /home/xiaobai/Downloads/my_icons/1/pika-hdpi/hot.png
    To: /home/xiaobai/AndroidStudioProjects/hello-world/app/src/main/res/drawable-hdpi 

    xb@dnxb:~/Downloads/misc/python/drawable-cp$ 

#### More info please check `--help`.

#### Caveat:
It only scan mdpi, hdpi, xhdpi, xxhdpi, and xxxhdpi, you should edit `drawable_valid_path_l_proj` and `drawable_valid_path_l_designer` tuples if want to add more.



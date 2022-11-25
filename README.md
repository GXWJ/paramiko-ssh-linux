说明：
    通过使用paramiko进行ssh连接可运行shell命令和上传下载文件

环境要求：
    python3
    paramiko库
    tkinter库

库安装：
1.安装paramiko，在cmd控制台执行pip命令安装豆瓣的paramiko源文件

    ``` shell
    pip3 install paramiko -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
    ```

2.安装python GUI tkinter,在cmd控制台运行

    ```shell
    pip install tkinterplus
    ```

注：
在pip install过程中可能会出现

   ```shell
   [notice] A new release of pip available: 22.3 -> 22.3.1
   [notice] To update, run: c:\users\wangj\appdata\local\programs\python\python38\python.exe -m pip install --upgrade pip
   ```

的报错，直接运行第二行run：后面的内容即示例中的  

``` shell
c:\users\wangj\appdata\local\programs\python\python38\python.exe -m pip install --upgrade pip
```

![image-20221125175448931](C:/Users/wangj/AppData/Roaming/Typora/typora-user-images/image-20221125175448931.png)
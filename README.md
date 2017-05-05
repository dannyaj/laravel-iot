# laravel-iot for Device dashboard Template

# Step 1 Build your own image
docker build -t laravel .

# Step 2 Start your laravel (this step will use the default laravel project)
$ docker run -d -p 80:80 laravel

# or Mount your project
$ docker run -d -p 80:80 -v $PROJECT_PATH:/var/www/laravel laravel

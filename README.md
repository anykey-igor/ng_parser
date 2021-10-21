#ng_parser
Parser Nginx log - this script parsing the Nginx log file, saves the result to a csv or json file of your choice and sends it to your GitHub repository


### Naming convention
* ng_parser.py - Script fro parsing log files.
* requirements.txt -  application dependency file
* Dockerfile - config file for building Docker image
* .gitconfig - config file for GitHub


##Using Nginx log format

```
log_format myformat '$remote_addr - - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```

##Usage:

### Requirements:

Use your credential for identification. Edit **_.gitconfig_**:

```editorconfig
[user]
  email = your_email
  name = your_name
[init]
  defaultbranch=main
```

Create new repository for this script in you GitHub account. Follow next instructions:
 
>https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository

To work with GItHub you need an active token. Follow next instruction to generate and activate GitHub token: 

>https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

After receiving the GitHub token, edit the Dockerfile: 

```dockerfile
# Enter your GitHub token
ENV GH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXX

# Enter your repository URL. For example - /your-login/your_repository.git
ENV REPO_URL=/your-login/your_repository.git
```

For run script in Docker image

* Installed Docker Engine on your server
* Clone project
> $ git clone https://github.com/anykey-igor/ng_parser
> 
> $ cd ng_parser/
* Build image
>$ docker build -t ng_parser:latest .


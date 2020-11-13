prerequesite

1. create Systems Manager Parameter on the console
/springboot-multiarch/dockerhub/username
/springboot-multiarch/dockerhub/password

2. 
```
python3 -m venv .env

cd cdk
./bootstrap.sh {account id}
```

commit code to codecommit

kubectl describe ingress | grep Address 

./cleanup.sh
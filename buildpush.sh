docker rmi syukurdocker/smart_speaker:latest
docker buildx build --platform=linux/arm64,linux/amd64 --push -t syukurdocker/smart_speaker:latest .
docker buildx rm $BUILDER

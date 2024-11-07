docker rmi syukurdocker/smart_speaker:latest
BUILDER=$(docker buildx create --use)
docker buildx build --platform=linux/arm/v7 --push -t syukurdocker/smart_speaker:latest .
docker buildx rm $BUILDER
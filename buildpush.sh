BUILDER=$(docker buildx create --use)
docker buildx build --platform=linux/arm/v7 --push -t syukurdocker/smart_speaker:latest .
docker buildx rm $BUILDER
docker system prune -y -a --volumes
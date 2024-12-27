#!/bin/bash
concurrency_level=$1
start_idx=$2
end_idx=$3

# 싱행 환경 - 도커 관련 변수
DOCKER_IMAGE="viral_scrapper"
DOCKER_TAG="latest"
FULL_IMAGE="$DOCKER_IMAGE:$DOCKER_TAG"

# 람다 스크래퍼 이미지 있는지 확인, 없으면 Dockerfile 빌드
if ! docker image inspect "$FULL_IMAGE" > /dev/null 2>&1; then
    echo "[INFO] Docker image '$FULL_IMAGE' not found. Building the image"
    docker build -t "$FULL_IMAGE" -f "$DOCKERFILE_PATH" .
else
    echo "[INFO] Docker image '$FULL_IMAGE' already exists. Skip building."
fi


# 컨테이너 하나 실행시켜서 람다 trigger
# pre-requistes : logs path, env file
run_container() {
    local brand_name=$1
    local port=$2
    local container_name=$3

    docker run -d -p $port:8080 \
        --env-file .env \
        -v ./src:/var/task/src \
        -v ./logs:/var/log \
        --name $container_name $FULL_IMAGE

    curl -X POST \
    -H "Content-Type: application/json" \
    -d "{
        \"user_agent\": \"Mozilla/5.0\",
        \"platform\": \"oliveyoung\",
        \"details\": {
            \"target\": \"item\",
            \"brand\": \"$brand_name\"
        } \
    }" \
    http://localhost:$port/2015-03-31/functions/function/invocations

    docker stop $container_name
    docker rm $container_name
    wait

    echo "[INFO] category $brand_name is finished in $container_name"
}


# 실행 대상 - 수집할 대상 브랜드 리스트 변수
BRAND_LIST_JSON_PATH="./src/youtube/config.json"
KEYWORDS=()
while IFS= read -r keyword; do
  KEYWORDS+=("$keyword")
done < <(jq -r ".keywords[$start_idx:$end_idx][]" "$BRAND_LIST_JSON_PATH")


if [ -z "$KEYWORDS" ]; then
    echo "[ERROR] No keywords found in the specified range."
    exit 1
else
    echo "[INFO] Start with brand keywords $KEYWORDS"
fi

# concurrency control - level 수만큼 컨테이너 동시에 실행
concurrency_level() {
    local level=$1
    local brand_list=$2
    
    for (( j=$level; j<${#brand_list[@]}; j+=$concurrency_level )); do
        brand=${brand_list[j]}
        port=$((8080 + level))
        run_container "$brand" "$port" "scrapping_container_${level}"
    done &
}

for (( i=0; i<=$concurrency_level; i+=1 )); do
    concurrency_level "$i" "$KEYWORDS"
done

# 모든 컨테이너 끝날때까지 대기
wait

echo "[INFO] All containers have completed execution."


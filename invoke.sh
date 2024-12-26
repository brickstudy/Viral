#!/bin/bash
concurrency_level=$1
start_idx=$2
end_idx=$3

echo "start with concur_lv $concurrency_level, list index $start_idx to $end_idx"

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

    echo "[INFO] Starting container $container_name for brand $brand_name on port $port"

    docker run -d -p $port:8080 \
        --env-file .env \
        -v ./src:/var/task/src \
        -v ./logs:/var/log \
        --name $container_name $FULL_IMAGE

    # 컨테이너가 완전히 시작될 때까지 대기
    echo "[INFO] Waiting for container to be ready..."
    sleep 10

    # API 호출
    echo "[INFO] Sending request to container..."
    # brand_name에서 특수문자 제거 (백슬래시, 따옴표 등)
    cleaned_brand_name=$(echo "$brand_name" | sed 's/[^[:alnum:]가-힣]//g')
    
    json_payload=$(printf '{"user_agent":"Mozilla/5.0","platform":"oliveyoung","details":{"target":"item","brand":"%s"}}' "$cleaned_brand_name")
    
    echo "[DEBUG] Sending payload: $json_payload"
    
    curl -X POST \
        -H "Content-Type: application/json" \
        -d "$json_payload" \
        http://localhost:$port/2015-03-31/functions/function/invocations

    # 컨테이너 응답 대기
    docker logs -f $container_name &
    
    # 컨테이너가 종료될 때까지 대기
    docker wait $container_name

    # 컨테이너 정리
    echo "[INFO] Cleaning up container $container_name"
    docker stop $container_name
    docker rm $container_name

    echo "[INFO] Brand $brand_name processing completed in $container_name"
}


# 실행 대상 - 수집할 대상 브랜드 리스트 변수
BRAND_LIST_JSON_PATH="./src/youtube/config.json"

# concurrency control - level 수만큼 컨테이너 동시에 실행
concurrency_level() {
    local level=$1
    local brand_list=($(jq ".keywords[$start_idx:$end_idx] | values[]" ${BRAND_LIST_JSON_PATH}))
    echo "in concur_function. lv $level brand_lst $brand_list"
    for (( j=$level; j<${#brand_list[@]}; j+=$concurrency_level )); do
        echo $j
        brand=${brand_list[j]} 
        port=$((8080 + level))
        echo "run container for $brand in port $port"
        run_container "$brand" "$port" "scrapping_container_${level}"
    done &
}

for (( i=0; i<=$concurrency_level; i+=1 )); do
    concurrency_level "$i"
done

# 모든 컨테이너 끝날때까지 대기
wait

echo "[INFO] All containers have completed execution."


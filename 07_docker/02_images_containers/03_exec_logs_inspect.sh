#!/bin/bash

# ============================================================
# Day 7 — Docker exec / logs / inspect
# File: 07_docker/02_images_containers/03_exec_logs_inspect.sh
#
# 목표
# - 실행 중인 컨테이너 내부에서 명령어를 실행하는 방법을 익힌다.
# - 컨테이너 로그를 확인하는 방법을 배운다.
# - 컨테이너 상세 설정 정보를 inspect로 조회하는 방법을 익힌다.
#
# 한국어 설명
# Day 6에서 pull / run / stop / rm을 배웠다면,
# Day 7에서는 "실행 중인 컨테이너를 관찰하는 방법"을 배운다.
#
# 핵심 명령어:
# 1) docker exec
# 2) docker logs
# 3) docker inspect
#
# 실습 흐름:
# - nginx 컨테이너 실행
# - logs 확인
# - exec로 내부 명령 실행
# - inspect로 상세 정보 확인
# - 마지막에 컨테이너 정리
# ============================================================


# ------------------------------------------------------------
# 0) 변수 정의
# ------------------------------------------------------------
IMAGE_NAME="nginx:latest"
CONTAINER_NAME="docker_day7_nginx"

echo "========================================"
echo "Docker Day 7 Practice Started"
echo "Image     : ${IMAGE_NAME}"
echo "Container : ${CONTAINER_NAME}"
echo "========================================"


# ------------------------------------------------------------
# 1) Docker 버전 확인
# ------------------------------------------------------------
echo
echo "[1] Checking Docker version..."
docker --version


# ------------------------------------------------------------
# 2) 기존 동일 이름 컨테이너 정리
# ------------------------------------------------------------
# 한국어 설명
# 같은 이름의 컨테이너가 이미 있으면 충돌이 날 수 있으므로
# 먼저 삭제한다.
echo
echo "[2] Removing existing container if present..."
docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true


# ------------------------------------------------------------
# 3) nginx 이미지 pull
# ------------------------------------------------------------
echo
echo "[3] Pulling image..."
docker pull "${IMAGE_NAME}"


# ------------------------------------------------------------
# 4) 컨테이너 실행
# ------------------------------------------------------------
# 한국어 설명
# nginx를 백그라운드에서 실행하고 8080 포트를 연결한다.
echo
echo "[4] Running container..."
docker run -d --name "${CONTAINER_NAME}" -p 8080:80 "${IMAGE_NAME}"


# ------------------------------------------------------------
# 5) 실행 중 컨테이너 확인
# ------------------------------------------------------------
echo
echo "[5] Checking running containers..."
docker ps


# ------------------------------------------------------------
# 6) docker logs
# ------------------------------------------------------------
# 한국어 설명
# nginx 컨테이너가 시작되면서 출력한 로그를 확인한다.
echo
echo "[6] Showing container logs..."
docker logs "${CONTAINER_NAME}"


# ------------------------------------------------------------
# 7) docker exec - 컨테이너 내부 명령 실행
# ------------------------------------------------------------
# 한국어 설명
# 컨테이너 내부에서 pwd 명령어를 실행
echo
echo "[7] Running 'pwd' inside the container..."
docker exec "${CONTAINER_NAME}" pwd

# 컨테이너 내부 파일 목록 확인
echo
echo "[8] Listing files inside /usr/share/nginx/html ..."
docker exec "${CONTAINER_NAME}" ls -l /usr/share/nginx/html


# ------------------------------------------------------------
# 8) docker inspect
# ------------------------------------------------------------
# 한국어 설명
# inspect는 컨테이너 상세 정보를 JSON으로 보여준다.
# 출력이 길기 때문에 전체보다는 일부만 확인하는 예제를 보여준다.
echo
echo "[9] Inspecting container (showing key sections)..."
docker inspect "${CONTAINER_NAME}"


# ------------------------------------------------------------
# 9) inspect에서 원하는 정보만 보기
# ------------------------------------------------------------
# 한국어 설명
# Go template을 사용하면 inspect 결과에서 원하는 값만 추출 가능
echo
echo "[10] Container status:"
docker inspect -f '{{.State.Status}}' "${CONTAINER_NAME}"

echo
echo "[11] Container IP address:"
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${CONTAINER_NAME}"

echo
echo "[12] Container image name:"
docker inspect -f '{{.Config.Image}}' "${CONTAINER_NAME}"

echo
echo "[13] Port bindings:"
docker inspect -f '{{json .HostConfig.PortBindings}}' "${CONTAINER_NAME}"


# ------------------------------------------------------------
# 10) 브라우저 안내
# ------------------------------------------------------------
echo
echo "[14] Open this URL in your browser:"
echo "     http://localhost:8080"


# ------------------------------------------------------------
# 11) 정리 (stop + rm)
# ------------------------------------------------------------
echo
echo "[15] Stopping container..."
docker stop "${CONTAINER_NAME}"

echo
echo "[16] Removing container..."
docker rm "${CONTAINER_NAME}"


# ------------------------------------------------------------
# 12) 최종 상태 확인
# ------------------------------------------------------------
echo
echo "[17] Final container list..."
docker ps -a


# ------------------------------------------------------------
# 13) 종료 메시지
# ------------------------------------------------------------
echo
echo "========================================"
echo "Docker Day 7 Practice Completed"
echo
echo "What you practiced:"
echo "- docker logs"
echo "- docker exec"
echo "- docker inspect"
echo
echo "Key concept:"
echo "A running container can be observed, inspected, and controlled."
echo "========================================"
import heapq
import math

def dijkstra(graph, r):
    # 시작 정점 r에서 각 정점까지의 거리를 무한대로 초기화 (아직 경로를 모름)
    dist = {v: math.inf for v in graph}
    # 모든 정점의 직전 정점을 none으로 초기화 (prev는 경로 복원을 위한 변수) -> 마지막에 prev를 거꾸로 따라가면 최단 경로가 복원됨
    prev = {v: None for v in graph}
    # 시작 정점의 거리만 0으로 설정
    dist[r] = 0

    # 우선순위 큐 초기화: (현재까지의 거리, 정점) 튜플 저장
    # heapq는 튜플 첫 번째 요소(거리) 기준 최소 힙 -> 거리가 작은 정점부터 pop
    pq = [(0,r)]
    # 확정된 정점 집합 (최단 거리가 확정된 정점들)
    S = set()

    # pq가 빌 때까지
    while pq:
        # 거리가 가장 짧은 정점을 꺼냄 - 이 시점에 u의 최단 거리가 확정됨
        d, u = heapq.heappop(pq)
        # 오래된 항목은 건너뛰기
        if u in S:
            continue
        # u를 확정 집합에 추가 (이후 u의 dist는 더 이상 갱신되지 않음)
        S.add(u)

        # u의 모든 인접 정점 v와 간선 가중치 w_uv에 대해 이완 시도
        for v, w_uv in graph[u]:
            # v가 아직 미확정이고 (S에 없음), u를 거치는 새 경로가 기존 dist[v]보다 작으면 
            if v not in S and dist[u] + w_uv < dist[v]:
                # 더 짧은 경로 발견 -> v까지의 최단 거리 갱신
                dist[v] = dist[u] + w_uv
                # 경로 복원용으로 v의 직전 정점을 u로 기록
                prev[v] = u
                # 갱신된 거리로 v를 우선순위 큐에 다시 push
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


# 예시
wg = {
    1: [(2, 10), (3, 5)],
    2: [(3, 2), (4, 1)],
    3: [(2, 3), (4, 9), (5, 2)],
    4: [(5, 4)],
    5: [(1, 7), (4, 6)],
}
dist, prev = dijkstra(wg, 1)
print(dist)        # {1: 0, 2: 8, 3: 5, 4: 9, 5: 7}
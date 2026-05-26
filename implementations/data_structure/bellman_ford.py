import math

def bellman_ford(graph, r):
    # 시작 정점 r에서 각 정점까지의 거리를 무한대로 초기화 (아직 경로를 모름)
    dist = {v: math.inf for v in graph}
    # 모든 정점의 직전 정점을 none으로 초기화 (prev는 경로 복원을 위한 변수) -> 마지막에 prev를 거꾸로 따라가면 최단 경로가 복원됨
    prev = {v: None for v in graph}
    # 시작 정점의 거리만 0으로 설정
    dist[r] = 0

    # 정점 리스트 (반복 횟수를 결정하는 데 사용)
    V = list(graph.keys())

    # 모든 간선을 (u, v, w_uv) 튜플로 펼쳐 평평한 리스트로 만듦
    # 이중 컴프리헨션: 바깥  루프(u) x 안쪽 루프((v,w) in graph[u])
    # 다음 루프에서 "모든 간선에 대해 이완"을 깔끔히 표현
    edges = [(u,v,w) for u in graph for (v, w) in graph[u]]

    # 이완 루프: 모든 간선을 V-1번 반복하여 이완
    for _ in range(len(V)-1):
        # 매 라운드마다 모든 간선을 순회하며 이완 시도
        for u, v, w_uv in edges:
            # u를 거치는 새 경로가 기존 dist[v]보다 짧으면
            if dist[u] + w_uv < dist[v]:
                # 더 짧은 경로 발견 -> v까지의 최단 거리 갱신
                dist[v] = dist[u] + w_uv
                #경로 복원용 : v의 직전 정점을 u로 기록
                prev[v] = u

    # 음의 사이클 감지 : V번째 라운드에서도 이완 가능한 간선이 있는 지 확인
    # 정상이라면 V-1 반복으로 이미 수렴
    # 또 이완되면 음의 사이클 존재
    for u,v,w_uv in edges:
        if dist[u] + w_uv < dist[v]:
            # 음의 사이클 발견 -> 최단 거리가 정의되지 않음(사이클 돌 때마다 무한히 감소 가능)
            return dist, prev, True
    # 음의 사이클 없음 -> 정상 종료, dist와 prev에 정확한 최단 거리/경로 정보가 담김
    return dist, prev, False


# 예시 (음수 간선 포함)
ng = {
    1: [(2, 6), (3, 7)],
    2: [(3, 8), (4, 5), (5, -4)],
    3: [(4, -3), (5, 9)],
    4: [(2, -2)],
    5: [(1, 2), (4, 7)],
}
dist, prev, neg = bellman_ford(ng, 1)
print(dist, neg)   # {1: 0, 2: 2, 3: 7, 4: 4, 5: -2} False
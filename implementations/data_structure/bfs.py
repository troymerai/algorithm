from collections import deque

def bfs(graph, s):
    #그래프의 전체 노드를 visited == false로 초기화
    visited = {v: False for v in graph}
    #시작점의 노드를 visited == true로 ㅅ ㅓㄹ정
    visited[s] = True
    # 노드 s를 Q라는 자료구조(덱)에 넣음
    Q = deque([s])
    # 노드를 방문한 순서를 담은 리스트 (나중에 반환)
    order = []

    # Q가 빌 때까지 진행
    while Q:
        # 덱에서 하나씩 꺼내서 u에 담음
        u = Q.popleft()
        # 큐에서 꺼낸 거를 순서에 order라는 배열에 넣음 (순회 순서를 저장)
        order.append(u)
        # Q에서 꺼낸 값에 대해서 인접 노드 확인
        for v in graph[u]:
            # u의 인접 노드 중에서 방문하지 않은 노드면
            if not visited[v]:
                # visited == true로 설정하고 Q에 넣기
                visited[v] = True
                Q.append(v)
    return order


g = {1: [2, 3], 2: [1, 4, 5], 3: [1, 6], 4: [2], 5: [2], 6: [3]}


print(bfs(g,1))


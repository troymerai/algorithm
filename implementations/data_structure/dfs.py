def dfs(graph, s):
    # 모든 노드를 visited = false로 초기화
    visited = {v: False for v in graph}
    # 시작 노드를 true로 설정
    visited[s] = True
    # 스택에 시작 노드 삽입
    stack = [s]                    
    # 방문 순서 기록 리스트
    order = []
    
    # 스택이 빌 때까지 반복
    while stack:
        # 스택에서 pop하여 u에 담기
        u = stack.pop()                  # ← popleft()가 아니라 "pop()" (뒤에서 꺼냄) 이게 종방향으로 내려가는 이유
        # 스택에서 pop한 값을 order리스트에 담기
        order.append(u)
        
        # 스택은 LIFO라 나중에 push된 노드가 먼저 pop됨
        # reversed로 거꾸로 push하면 → 앞쪽 인접 노드부터 깊이 탐색 (재귀형과 동일한 순서)      
        for v in reversed(graph[u]):
            print(graph[u])
            # 방문하지 않은 노드가 있다면
            if not visited[v]:
                # 방문 처리하고 스택에 집어 넣기
                visited[v] = True
                stack.append(v)       
    return order


g = {1: [2, 3], 2: [1, 4, 5], 3: [1, 6], 4: [2], 5: [2], 6: [3]}
print(dfs(g, 1))
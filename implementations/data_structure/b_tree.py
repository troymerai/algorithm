"""
=============================================================
 B-트리 (B-Tree) 구현 가이드
=============================================================
 핵심 개념:
   - 균형 잡힌 다진(multi-way) 검색 트리
   - 디스크 기반 데이터 구조 (한 노드 = 한 디스크 블록)
   - 모든 리프가 같은 깊이 (작년 문제 (11): 참!)

 차수 t (최소 차수, minimum degree):
   - 루트 외 각 노드의 키 수: t-1 ≤ keys ≤ 2t-1
   - 루트의 키 수: 1 ≤ keys ≤ 2t-1
   - 자식 수: t ≤ children ≤ 2t (루트 제외)

 시간복잡도:
   검색 / 삽입 / 삭제 : O(log n)
   (정확히는 O(t · log_t(n)), t는 상수로 취급)

 공간복잡도: O(n)

 시험 포인트:
   - 작년 3번: 한 노드의 최대 키 수 계산 (풀이 포함!)
   - 작년 (11)번: 모든 리프가 동일 깊이 → 참
   - 작년 (12)번: 그리드 파일은 트리 구조? → 거짓 (격자 구조)
=============================================================
"""


class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []          # 키 리스트
        self.children = []      # 자식 노드 리스트
        self.leaf = leaf        # 리프 노드 여부


class BTree:
    def __init__(self, t):
        """
        t: 최소 차수 (minimum degree)
        각 노드는 최대 2t-1개의 키, 최대 2t개의 자식
        """
        self.t = t
        self.root = BTreeNode(leaf=True)
    
    # ─────────────────────────────────────────
    #  검색 : O(t · log_t(n))
    # ─────────────────────────────────────────
    def search(self, key, node=None):
        """
        BST 검색과 유사하지만, 각 노드에서 여러 키를 비교

        예시 (t=2, 각 노드 최대 3키):
        
             [10, 20]
            /   |    \
        [3,5] [12,15] [25,30,35]
        
        key=15 검색:
        1) 루트 [10,20]: 10<15<20 → 가운데 자식으로
        2) [12,15]: 15 발견!
        """
        if node is None:
            node = self.root
        
        i = 0
        # 현재 노드에서 key보다 크거나 같은 첫 키 찾기
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # 키를 찾은 경우
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)
        
        # 리프인데 못 찾은 경우
        if node.leaf:
            return None
        
        # 적절한 자식으로 내려감
        return self.search(key, node.children[i])
    
    # ─────────────────────────────────────────
    #  삽입
    # ─────────────────────────────────────────
    def insert(self, key):
        """
        삽입 전략: 내려가면서 가득 찬 노드는 미리 분할
        
        예시 (t=2, 최대 3키):
        
        [10, 20, 30]에 25 삽입 시:
        
        1) 노드가 가득 참 → 분할
            [10, 20, 30]  →    [20]
                              /    \
                           [10]   [30]
        
        2) 25는 30의 왼쪽에 삽입
                  [20]
                 /    \
              [10]   [25, 30]
        """
        root = self.root
        
        # 루트가 가득 찬 경우 → 루트 분할
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key)
    
    def _split_child(self, parent, i):
        """
        parent의 i번째 자식이 가득 찼을 때 분할

        t=2일 때:
        가득 찬 자식: [A, B, C]
        → 중간값 B를 부모로 올리고
        → [A]와 [C]로 분할
        """
        t = self.t
        full_child = parent.children[i]
        new_child = BTreeNode(leaf=full_child.leaf)
        
        # 중간 키
        mid_key = full_child.keys[t - 1]
        
        # 오른쪽 절반의 키를 새 노드로
        new_child.keys = full_child.keys[t:]
        full_child.keys = full_child.keys[:t - 1]
        
        # 리프가 아니면 자식도 분할
        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]
        
        # 부모에 중간 키 삽입
        parent.keys.insert(i, mid_key)
        parent.children.insert(i + 1, new_child)
    
    def _insert_non_full(self, node, key):
        """가득 차지 않은 노드에 삽입"""
        i = len(node.keys) - 1
        
        if node.leaf:
            # 리프 노드: 올바른 위치에 삽입
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            # 내부 노드: 적절한 자식 찾기
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # 자식이 가득 찼으면 미리 분할
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_non_full(node.children[i], key)
    
    # ─────────────────────────────────────────
    #  삭제
    # ─────────────────────────────────────────
    def delete(self, key):
        self._delete(self.root, key)
        # 루트가 비었으면 자식을 새 루트로
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]
    
    def _delete(self, node, key):
        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if node.leaf:
            # Case 1: 리프 노드에서 삭제
            if i < len(node.keys) and node.keys[i] == key:
                node.keys.pop(i)
            return
        
        if i < len(node.keys) and node.keys[i] == key:
            # Case 2: 내부 노드에서 삭제
            if len(node.children[i].keys) >= t:
                # Case 2a: 왼쪽 자식에서 직전원소로 대체
                pred = self._get_predecessor(node, i)
                node.keys[i] = pred
                self._delete(node.children[i], pred)
            elif len(node.children[i + 1].keys) >= t:
                # Case 2b: 오른쪽 자식에서 후속원소로 대체
                succ = self._get_successor(node, i)
                node.keys[i] = succ
                self._delete(node.children[i + 1], succ)
            else:
                # Case 2c: 양쪽 자식 합치기
                self._merge(node, i)
                self._delete(node.children[i], key)
        else:
            # Case 3: 키가 이 노드에 없으면 자식으로 내려감
            if len(node.children[i].keys) < t:
                self._fill(node, i)
                # fill 후 인덱스 조정
                if i > len(node.keys):
                    i -= 1
            self._delete(node.children[i], key)
    
    def _get_predecessor(self, node, i):
        """왼쪽 서브트리의 최대값"""
        current = node.children[i]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]
    
    def _get_successor(self, node, i):
        """오른쪽 서브트리의 최소값"""
        current = node.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]
    
    def _merge(self, node, i):
        """node.children[i]와 node.children[i+1]을 합치기"""
        left = node.children[i]
        right = node.children[i + 1]
        
        left.keys.append(node.keys[i])
        left.keys.extend(right.keys)
        if not left.leaf:
            left.children.extend(right.children)
        
        node.keys.pop(i)
        node.children.pop(i + 1)
    
    def _fill(self, node, i):
        """자식의 키가 t-1개일 때 보충"""
        if i > 0 and len(node.children[i - 1].keys) >= self.t:
            self._borrow_from_prev(node, i)
        elif i < len(node.children) - 1 and len(node.children[i + 1].keys) >= self.t:
            self._borrow_from_next(node, i)
        else:
            if i < len(node.keys):
                self._merge(node, i)
            else:
                self._merge(node, i - 1)
    
    def _borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i - 1]
        
        child.keys.insert(0, node.keys[i - 1])
        node.keys[i - 1] = sibling.keys.pop()
        
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
    
    def _borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        
        child.keys.append(node.keys[i])
        node.keys[i] = sibling.keys.pop(0)
        
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
    
    # ─────────────────────────────────────────
    #  시각화
    # ─────────────────────────────────────────
    def display(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        
        print(f"{'  ' * level}{prefix}{node.keys}")
        
        if not node.leaf:
            for i, child in enumerate(node.children):
                self.display(child, level + 1, f"Child[{i}]: ")
    
    def inorder(self, node=None):
        if node is None:
            node = self.root
        result = []
        for i in range(len(node.keys)):
            if not node.leaf:
                result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])
        if not node.leaf:
            result.extend(self.inorder(node.children[-1]))
        return result


"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 시험 대비: 작년 3번 — B-트리 최대 키 수 계산
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

조건:
  - 블록 크기: 4,096 바이트
  - 키 크기: 10 바이트
  - 페이지 번호(포인터): 8 바이트
  - 부모 링크: 있음 (8바이트)

한 노드 구조:
  [부모링크] + [자식포인터₀][키₁][자식포인터₁][키₂]...[키ₘ][자식포인터ₘ]

키가 m개이면:
  - 자식 포인터: m+1 개 × 8바이트
  - 키: m 개 × 10바이트
  - 부모 링크: 1 × 8바이트

총: 8(m+1) + 10m + 8 ≤ 4096
    8m + 8 + 10m + 8 ≤ 4096
    18m + 16 ≤ 4096
    18m ≤ 4080
    m ≤ 226.67

→ 최대 키 수 = 226개
"""


# ── 테스트 ──
if __name__ == "__main__":
    print("=" * 50)
    print(" B-트리 (t=2, 즉 2-3-4 트리)")
    print("=" * 50)
    
    bt = BTree(t=2)   # t=2: 노드당 키 1~3개, 자식 2~4개
    
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for k in keys:
        bt.insert(k)
        print(f"\n{k} 삽입 후:")
        bt.display()
    
    print(f"\n중위순회: {bt.inorder()}")
    
    # 삭제 테스트
    print("\n" + "=" * 50)
    print(" 6 삭제")
    print("=" * 50)
    bt.delete(6)
    bt.display()
    print(f"중위순회: {bt.inorder()}")
    
    # ── 작년 문제 3번 계산 검증 ──
    print("\n" + "=" * 50)
    print(" 작년 문제 3번: B-트리 최대 키 수")
    print("=" * 50)
    
    block_size = 4096
    key_size = 10
    pointer_size = 8
    parent_link = 8      # 부모 포인터
    
    # 18m + 16 <= 4096
    m = (block_size - parent_link - pointer_size) // (key_size + pointer_size)
    print(f"블록: {block_size}B, 키: {key_size}B, 포인터: {pointer_size}B")
    print(f"계산: (4096 - 8 - 8) / (10 + 8) = {(block_size - parent_link - pointer_size) / (key_size + pointer_size):.2f}")
    print(f"최대 키 수: {m}개")
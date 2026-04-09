r"""
=============================================================
 레드블랙 트리 (Red-Black Tree) 구현 가이드
=============================================================
 핵심 속성 (5가지 — 반드시 암기):
   1) 모든 노드는 빨강(R) 또는 검정(B)
   2) 루트는 항상 검정(B)
   3) 모든 리프(NIL)는 검정(B)
   4) 빨간 노드의 자식은 반드시 검정 (빨강 연속 불가!)
   5) 임의의 노드에서 리프까지의 모든 경로에서
      검정 노드의 수(Black Height)가 같다

 시간복잡도:
   검색 / 삽입 / 삭제 : 모두 O(log n)

 공간복잡도: O(n)

 시험 포인트 (작년 5번):
   - 삽입 후 회전(rotation) + 색 변경 과정을 그릴 수 있어야 함
   - 삭제 시 "직전원소(predecessor)로 대치" 후 조정
   - 노드에 r/b를 반드시 명시


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 삭제 fixup 케이스별 핵심 요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 지워진 노드가 Black이면 그 경로의 Black 개수가 1개 줄어
 5번 규칙에 어긋난다. 빈자리를 채우러 올라온 노드에게
 엑스트라 블랙(Extra Black)을 부여한다.

 ■ 올라온 애가 Red → Red + Extra Black = 그냥 Black으로 칠하면 끝
 ■ 올라온 애가 Black → Black + Extra Black = 이중 흑색(Double Black, DB)
   → DB의 Extra Black을 없애기 위해 형제 노드 상태에 따라 4가지 케이스 처리

 ※ 회전 방향 규칙:
    DB가 부모의 왼쪽 자식이면 → 부모 기준 좌회전 (left rotate)
    DB가 부모의 오른쪽 자식이면 → 부모 기준 우회전 (right rotate)
    즉, DB를 위로 끌어올리는 방향으로 회전한다고 생각하면 됨

 ┌────────┬───────────────────────────────┬──────────────────────────────────┐
 │ Case 1 │ 형제가 Red                     │ 형제→Black, 부모→Red,             │
 │        │                               │ 부모 기준 회전.                    │
 │        │                               │ (DB가 왼쪽이면 좌회전,             │
 │        │                               │  DB가 오른쪽이면 우회전)            │
 │        │                               │ DB의 새 형제가 Black이 되어        │
 │        │                               │ Case 2/3/4로 상황이 바뀐다.        │
 ├────────┼───────────────────────────────┼──────────────────────────────────┤
 │ Case 2 │ 형제 Black,                    │ 형제의 Black을 뺏어 부모에게 준다    │
 │        │ 형제의 양쪽 자식 모두 Black      │ (형제→Red). DB의 Extra Black도    │
 │        │                               │ 부모에게 넘긴다.                   │
 │        │                               │ 부모가 원래 Red → Black 칠하고 끝   │
 │        │                               │ 부모가 원래 Black → 부모가 새 DB,   │
 │        │                               │ 부모 위치에서 다시 케이스 판별.      │
 │        │                               │ (회전 없음!)                      │
 ├────────┼───────────────────────────────┼──────────────────────────────────┤
 │ Case 3 │ 형제 Black,                    │ 형제와 안쪽 자식의 색을 바꾼다       │
 │        │ 안쪽 자식 Red + 바깥쪽 자식 Black│ (형제→Red, 안쪽→Black).           │
 │        │                               │ 형제 기준 회전.                    │
 │        │                               │ (DB가 왼쪽이면 형제를 우회전,       │
 │        │                               │  DB가 오른쪽이면 형제를 좌회전)      │
 │        │                               │ → Case 4 형태로 강제 변환.         │
 ├────────┼───────────────────────────────┼──────────────────────────────────┤
 │ Case 4 │ 형제 Black,                    │ 형제→부모색, 부모→Black,           │
 │        │ 바깥쪽 자식 Red                 │ 바깥쪽 자식→Black.                │
 │        │                               │ 부모 기준 회전.                    │
 │        │                               │ (DB가 왼쪽이면 좌회전,             │
 │        │                               │  DB가 오른쪽이면 우회전)            │
 │        │                               │ Extra Black이 완전히 소멸.         │
 │        │                               │ 삭제 종료.                        │
 └────────┴───────────────────────────────┴──────────────────────────────────┘

 ※ 안쪽/바깥쪽이란?
    DB가 왼쪽 자식일 때: 형제의 왼쪽 = 안쪽, 형제의 오른쪽 = 바깥쪽
    DB가 오른쪽 자식일 때: 형제의 오른쪽 = 안쪽, 형제의 왼쪽 = 바깥쪽
    (DB에서 가까운 쪽이 안쪽, 먼 쪽이 바깥쪽)
=============================================================
"""

RED = 'R'
BLACK = 'B'


class RBNode:
    """레드블랙 트리의 노드"""
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color      # 새 노드는 항상 빨강으로 삽입!
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        # NIL 노드 (센티넬) — 모든 리프를 대표
        self.NIL = RBNode(key=None, color=BLACK)
        self.root = self.NIL

    # ─────────────────────────────────────────
    #  검색 : 일반 BST와 동일, O(log n)
    # ─────────────────────────────────────────
    def search(self, key):
        node = self.root
        while node != self.NIL:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    # ─────────────────────────────────────────
    #  회전 연산 (삽입/삭제의 핵심 도구)
    # ─────────────────────────────────────────
    def _left_rotate(self, x):
        r"""
        왼쪽 회전 (좌회전):
            x                y
           / \     →       / \
          a   y           x   c
             / \         / \
            b   c       a   b
        """
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        r"""
        오른쪽 회전 (우회전):
            y              x
           / \    →      / \
          x   c         a   y
         / \               / \
        a   b             b   c
        """
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    # ─────────────────────────────────────────
    #  삽입
    # ─────────────────────────────────────────
    def insert(self, key):
        """
        삽입 과정:
        1) BST 삽입 (새 노드는 빨강)
        2) 레드블랙 속성 위반 시 fix-up
        """
        new_node = RBNode(key, RED)
        new_node.left = self.NIL
        new_node.right = self.NIL

        # 1단계: 일반 BST 삽입
        parent = None
        current = self.root
        while current != self.NIL:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # 2단계: fix-up
        self._insert_fixup(new_node)

    def _insert_fixup(self, z):
        """
        삽입 후 수정 — 3가지 케이스

        위반 조건: z와 z.parent가 둘 다 빨강 (4번 규칙 위반)

        ┌─────────────────────────────────────────┐
        │ Case 1: 삼촌(uncle)이 빨강               │
        │   → 부모, 삼촌→Black, 조부모→Red          │
        │   → 조부모에서 다시 검사                   │
        │                                         │
        │ Case 2: 삼촌이 Black + z가 안쪽 자식       │
        │   → 부모 기준 회전 → Case 3 형태로 강제 변환│
        │                                         │
        │ Case 3: 삼촌이 Black + z가 바깥쪽 자식     │
        │   → 부모→Black, 조부모→Red                │
        │   → 조부모 기준 회전. 삽입 종료.            │
        └─────────────────────────────────────────┘
        """
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right

                if uncle.color == RED:
                    # ── Case 1: 삼촌이 빨강 ──
                    # 부모, 삼촌→Black, 조부모→Red (색 변경만, 회전 없음!)
                    # z를 조부모로 이동시켜 다시 케이스 판별
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # ── Case 2: 삼촌 Black + z가 안쪽 자식 ──
                        # 부모 기준 좌회전 → Case 3 형태로 강제 변환
                        z = z.parent
                        self._left_rotate(z)
                    # ── Case 3: 삼촌 Black + z가 바깥쪽 자식 ──
                    # 부모→Black, 조부모→Red, 조부모 기준 우회전
                    # 삽입 종료.
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                # ══ 대칭 (부모가 오른쪽 자식인 경우) ══
                uncle = z.parent.parent.left

                if uncle.color == RED:
                    # Case 1 대칭: 색 변경만
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        # Case 2 대칭: 부모 기준 우회전 → Case 3으로
                        z = z.parent
                        self._right_rotate(z)
                    # Case 3 대칭: 조부모 기준 좌회전. 삽입 종료.
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)

        self.root.color = BLACK  # 속성 2: 루트는 항상 검정!

    # ─────────────────────────────────────────
    #  삭제
    # ─────────────────────────────────────────
    def _transplant(self, u, v):
        """u의 위치에 v를 대체"""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _tree_maximum(self, node):
        """서브트리의 최대값 (직전원소 찾기용)"""
        while node.right != self.NIL:
            node = node.right
        return node

    def _tree_minimum(self, node):
        """서브트리의 최소값"""
        while node.left != self.NIL:
            node = node.left
        return node

    def delete(self, key):
        """
        삭제 과정:
        1) BST와 똑같이 데이터를 지운다 (직전원소로 대치 — 시험 조건!)
        2) 지워진 노드가 Red → 규칙에 영향 없으므로 끝
        3) 지워진 노드가 Black → 5번 규칙 위반 → fix-up
        """
        z = self.search(key)
        if z is None:
            return

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            # 직전원소(predecessor)로 대치 — 시험 조건!
            y = self._tree_maximum(z.left)  # 왼쪽 서브트리의 최대
            y_original_color = y.color
            x = y.left

            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.left)
                y.left = z.left
                y.left.parent = y

            self._transplant(z, y)
            y.right = z.right
            y.right.parent = y
            y.color = z.color

        if y_original_color == BLACK:
            # 지워진 노드가 Black → 그 경로의 Black 개수가 1개 줄어듦
            # 빈자리를 채우러 올라온 x에게 엑스트라 블랙(Extra Black) 부여
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        """
        삭제 후 수정

        x = 빈자리를 채우러 올라온 노드 (Extra Black을 가진 상태)

        올라온 애가 Red → Red + Extra Black = 그냥 Black으로 칠하면 끝
        올라온 애가 Black → 이중 흑색(Double Black, DB) 상태
        → DB의 Extra Black을 없애기 위해 형제 상태에 따라 4가지 케이스 처리
        """
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                # x(DB)가 부모의 왼쪽 자식인 경우
                sibling = x.parent.right

                # ──────────────────────────────────────────────
                # Case 1: 형제가 Red
                # ──────────────────────────────────────────────
                # 형제→Black, 부모→Red
                # 부모 기준 좌회전 (DB가 왼쪽이므로)
                # → DB의 새 형제가 Black이 되어
                #   Case 2/3/4로 상황이 바뀐다.
                if sibling.color == RED:
                    sibling.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    sibling = x.parent.right

                # ──────────────────────────────────────────────
                # Case 2: 형제 Black, 형제의 양쪽 자식 모두 Black
                # ──────────────────────────────────────────────
                # 형제의 Black을 뺏어 부모에게 준다 (형제→Red)
                # DB의 Extra Black도 부모에게 넘긴다.
                # 부모가 원래 Red → Black으로 칠하고 끝
                # 부모가 원래 Black → 부모가 새 DB,
                #   부모 위치에서 다시 케이스 판별
                # (회전 없음!)
                if sibling.left.color == BLACK and sibling.right.color == BLACK:
                    sibling.color = RED
                    x = x.parent
                else:
                    # ──────────────────────────────────────────
                    # Case 3: 형제 Black,
                    #   안쪽(왼쪽) 자식 Red + 바깥쪽(오른쪽) 자식 Black
                    # ──────────────────────────────────────────
                    # 형제와 안쪽 자식의 색을 바꾼다
                    #   (형제→Red, 안쪽→Black)
                    # 형제 기준 우회전 (DB가 왼쪽이므로)
                    # → Case 4 형태로 강제 변환
                    if sibling.right.color == BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self._right_rotate(sibling)
                        sibling = x.parent.right

                    # ──────────────────────────────────────────
                    # Case 4: 형제 Black, 바깥쪽(오른쪽) 자식 Red
                    # ──────────────────────────────────────────
                    # 형제→부모색, 부모→Black, 바깥쪽 자식→Black
                    # 부모 기준 좌회전 (DB가 왼쪽이므로)
                    # → Extra Black이 완전히 소멸. 삭제 종료.
                    sibling.color = x.parent.color
                    x.parent.color = BLACK
                    sibling.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                # ══════════════════════════════════════════════
                # 대칭: x(DB)가 부모의 오른쪽 자식인 경우
                # 위의 Case 1~4를 좌우 반전하여 동일하게 적용
                # ══════════════════════════════════════════════
                sibling = x.parent.left

                # Case 1 대칭: 형제가 Red
                # 형제→Black, 부모→Red, 부모 기준 우회전 (DB가 오른쪽이므로)
                if sibling.color == RED:
                    sibling.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    sibling = x.parent.left

                # Case 2 대칭: 형제 Black, 양쪽 자식 모두 Black
                # 형제의 Black을 뺏어 부모에게 준다 (형제→Red)
                # (회전 없음!)
                if sibling.right.color == BLACK and sibling.left.color == BLACK:
                    sibling.color = RED
                    x = x.parent
                else:
                    # Case 3 대칭: 안쪽(오른쪽) 자식 Red + 바깥쪽(왼쪽) 자식 Black
                    # 형제→Red, 안쪽→Black, 형제 기준 좌회전 (DB가 오른쪽이므로)
                    # → Case 4 형태로 강제 변환
                    if sibling.left.color == BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self._left_rotate(sibling)
                        sibling = x.parent.left

                    # Case 4 대칭: 바깥쪽(왼쪽) 자식 Red
                    # 형제→부모색, 부모→Black, 바깥쪽→Black
                    # 부모 기준 우회전 (DB가 오른쪽이므로)
                    # → Extra Black이 완전히 소멸. 삭제 종료.
                    sibling.color = x.parent.color
                    x.parent.color = BLACK
                    sibling.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root

        # 올라온 애가 Red → Red + Extra Black = 그냥 Black으로 칠하면 끝
        x.color = BLACK

    # ─────────────────────────────────────────
    #  시각화 (트리 출력)
    # ─────────────────────────────────────────
    def display(self):
        """트리를 보기 좋게 출력"""
        lines = []
        self._display_helper(self.root, "", True, lines)
        print("\n".join(lines))

    def _display_helper(self, node, prefix, is_last, lines):
        if node == self.NIL:
            return

        connector = "└── " if is_last else "├── "
        color_str = f"({node.color})"
        lines.append(f"{prefix}{connector}{node.key}{color_str}")

        new_prefix = prefix + ("    " if is_last else "│   ")

        children = []
        if node.left != self.NIL:
            children.append(('L', node.left))
        if node.right != self.NIL:
            children.append(('R', node.right))

        for i, (side, child) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            self._display_helper(child, new_prefix, is_last_child, lines)

    def inorder(self):
        """중위 순회 결과 반환"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node != self.NIL:
            self._inorder(node.left, result)
            result.append(f"{node.key}({node.color})")
            self._inorder(node.right, result)


# ── 테스트: 작년 시험 5번 재현 ──
if __name__ == "__main__":
    print("=" * 50)
    print(" 작년 시험 [보기] 상태 구성")
    print("=" * 50)

    # 보기 트리 구성: 50(B), 20(B), 70(B), 10(R), 25(R)
    rbt = RedBlackTree()
    for key in [50, 20, 70, 10, 25]:
        rbt.insert(key)

    print("\n[보기 상태]")
    rbt.display()
    print(f"중위순회: {rbt.inorder()}")

    # ── (1) 8 삽입 ──
    print("\n" + "=" * 50)
    print(" (1) 8 삽입 후")
    print("=" * 50)

    rbt1 = RedBlackTree()
    for key in [50, 20, 70, 10, 25]:
        rbt1.insert(key)
    rbt1.insert(8)

    print()
    rbt1.display()
    print(f"중위순회: {rbt1.inorder()}")

    # ── (2) 50 삭제 ──
    print("\n" + "=" * 50)
    print(" (2) 50 삭제 후 (직전원소 25로 대치)")
    print("=" * 50)

    rbt2 = RedBlackTree()
    for key in [50, 20, 70, 10, 25]:
        rbt2.insert(key)
    rbt2.delete(50)

    print()
    rbt2.display()
    print(f"중위순회: {rbt2.inorder()}")
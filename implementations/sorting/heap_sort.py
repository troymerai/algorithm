"""
=============================================================
 힙 정렬 (Heap Sort) 구현 가이드
=============================================================
 핵심 아이디어:
   1) 배열을 최대 힙(Max Heap)으로 구성한다 (Build Heap)
   2) 루트(최대값)를 배열 끝으로 보내고 힙 크기를 줄인다
   3) 줄어든 힙에 대해 heapify를 반복한다

 최대 힙 성질:
   - 완전 이진 트리
   - 부모 노드 >= 자식 노드 (항상)
   - 배열 인덱스 관계 (0-based):
     부모: (i - 1) // 2
     왼쪽 자식: 2 * i + 1
     오른쪽 자식: 2 * i + 2

 시간복잡도:
   Best / Average / Worst : 모두 O(n log n)
   Build Heap: O(n)
   각 원소를 heapify: O(log n) * n번

 공간복잡도: O(1) — In-place 정렬
 안정성:     Unstable (heapify 과정에서 같은 값의 순서가 바뀔 수 있음)

 시험 포인트:
   - 항상 O(n log n) 보장 (퀵정렬과 다르게 최악이 없음)
   - In-place이지만 Unstable
   - heapify의 동작 과정을 손으로 그릴 수 있어야 함
=============================================================
"""


def heapify(arr, n, i):
    """
    i번째 노드를 루트로 하는 서브트리를 최대 힙으로 만든다
    트리 높이만큼 내려가면서 재귀호출하므로 시간복잡도는 O(log n)

    예시: arr = [4, 10, 3, 5, 1], n=5, i=0

        4          10
       / \   →    / \
      10  3      5   3
     / \        / \
    5   1      4   1

    i=0: largest=0
      왼쪽(1)=10 > 4 → largest=1
      오른쪽(2)=3 < 10 → largest=1
      swap(arr[0], arr[1]) → [10, 4, 3, 5, 1]
      재귀: heapify(arr, 5, 1)

    i=1: largest=1
      왼쪽(3)=5 > 4 → largest=3
      오른쪽(4)=1 < 5 → largest=3
      swap(arr[1], arr[3]) → [10, 5, 3, 4, 1]
    """
    largest = i            # 현재 노드를 최대값으로 가정
    left = 2 * i + 1       # 왼쪽 자식 인덱스
    right = 2 * i + 2      # 오른쪽 자식 인덱스

    # 왼쪽 자식이 현재 최대값보다 크면
    if left < n and arr[left] > arr[largest]:
        largest = left

    # 오른쪽 자식이 현재 최대값보다 크면
    if right < n and arr[right] > arr[largest]:
        largest = right

    # 최대값이 현재 노드가 아니면 교환 후 재귀
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    """
    전체 과정:

    원본: [4, 10, 3, 5, 1]

    ── 1단계: Build Max Heap ──
    마지막 내부 노드부터 역순으로 heapify
    내부 노드 인덱스: n//2 - 1 부터 0까지

    결과: [10, 5, 3, 4, 1]  (최대 힙)

    ── 2단계: 하나씩 추출 ──
    i=4: swap(10,1) → [1, 5, 3, 4, |10] → heapify → [5, 4, 3, 1, |10]
    i=3: swap(5,1)  → [1, 4, 3, |5, 10]  → heapify → [4, 1, 3, |5, 10]
    i=2: swap(4,3)  → [3, 1, |4, 5, 10]  → heapify → [3, 1, |4, 5, 10]
    i=1: swap(3,1)  → [1, |3, 4, 5, 10]  → heapify → [1, 3, 4, 5, 10]

    완성: [1, 3, 4, 5, 10]
    """
    n = len(arr)

    # 1단계: Build Max Heap
    # 마지막 내부 노드 = n // 2 - 1
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 2단계: 루트(최대값)를 끝으로 보내고 힙 크기 줄이기
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]   # 루트 ↔ 마지막 원소
        heapify(arr, i, 0)                # 줄어든 힙에서 heapify

    return arr


"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Build Heap이 O(n)인 이유
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

직관적으로 O(n log n)일 것 같지만, 실제로는 O(n)이다.

높이 h인 노드 수 × heapify 비용:
  높이 0 (리프):     n/2개  ×  0번 비교  =  0
  높이 1:            n/4개  ×  1번 비교  =  n/4
  높이 2:            n/8개  ×  2번 비교  =  n/4
  ...
  높이 log n (루트):  1개   × log n 비교 =  log n

총합: Σ(h=0 to log n) n/(2^(h+1)) × h
    = n × Σ h/2^(h+1)
    ≤ n × 2
    = O(n)

아래쪽 노드가 많지만 비교 횟수가 적고,
위쪽 노드는 비교가 많지만 수가 적어서 상쇄된다.
"""


# ── 테스트 ──
if __name__ == "__main__":
    test_cases = [
        [4, 10, 3, 5, 1],
        [12, 11, 13, 5, 6, 7],
        [1, 2, 3, 4, 5],           # 이미 정렬됨
        [5, 4, 3, 2, 1],           # 역순
        [3, 1, 4, 1, 5, 9, 2, 6],  # 중복 포함
    ]

    for tc in test_cases:
        original = tc.copy()
        result = heap_sort(tc)
        print(f"{original} → {result}")
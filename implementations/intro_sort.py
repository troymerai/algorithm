"""
Introsort (Introspective Sort)
==============================
상황              알고리즘     이유
-----------       ---------    ----------------------------------
원소 <= 16        삽입 정렬    소규모에서 오버헤드 없이 빠름
재귀 깊이 초과    힙 정렬      최악 O(n²) 방지, O(n log n) 보장
일반              퀵 정렬      평균적으로 가장 빠름

==============================

퀵 정렬의 O(n²) 최악 케이스를 힙 정렬로 방어하면서, 소규모 구간은 삽입 정렬로 상수 시간을 줄이는 거예요. 세 알고리즘의 장점만 취하는 구조

"""


# ── 삽입 정렬 ──────────────────────────────────────────────────
def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ── 힙 정렬 ───────────────────────────────────────────────────
def heapify(arr, n, i, offset):
    """arr[offset:offset+n] 범위에서 인덱스 i를 루트로 하는 서브트리를 heapify"""
    largest = i
    left  = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[offset + left] > arr[offset + largest]:
        largest = left
    if right < n and arr[offset + right] > arr[offset + largest]:
        largest = right

    if largest != i:
        arr[offset + i], arr[offset + largest] = arr[offset + largest], arr[offset + i]
        heapify(arr, n, largest, offset)


def heap_sort(arr, low, high):
    n = high - low + 1

    # 최대 힙 구성
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, low)

    # 하나씩 추출
    for i in range(n - 1, 0, -1):
        arr[low], arr[low + i] = arr[low + i], arr[low]
        heapify(arr, i, 0, low)


# ── 퀵 정렬 파티션 ────────────────────────────────────
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ── Introsort 본체 ─────────────────────────────────────────────
def introsort(arr, low, high, depth_limit):
    size = high - low + 1

    # 원소가 16개 이하면 삽입 정렬
    # 재귀 오버헤드 없이 소규모 배열을 빠르게 처리
    if size <= 16:
        insertion_sort(arr, low, high)
        return

    # 재귀 깊이가 한계에 도달하면 힙 정렬로 전환
    # 퀵 정렬이 계속 불균형 분할을 일으키고 있다는 신호 → O(n²) 방지
    if depth_limit == 0:
        heap_sort(arr, low, high)
        return

    # 일반적인 경우: 퀵 정렬 수행
    # partition()은 pivot을 올바른 위치에 놓고 그 인덱스를 반환
    # pivot 기준 왼쪽은 pivot보다 작은 원소, 오른쪽은 큰 원소
    pivot_idx = partition(arr, low, high)

    # pivot을 제외한 왼쪽/오른쪽 구간을 각각 재귀 호출
    # depth_limit을 1씩 줄여서 재귀 깊이를 추적
    introsort(arr, low, pivot_idx - 1, depth_limit - 1)   # pivot 왼쪽
    introsort(arr, pivot_idx + 1, high, depth_limit - 1)  # pivot 오른쪽


def sort(arr):
    if len(arr) <= 1:
        return arr

    # depth_limit = 2 * log2(n)
    # 균등 분할 시 퀵 정렬의 재귀 깊이는 log2(n)이므로
    # 그 2배를 초과하면 불균형 분할이 반복되고 있다고 판단
    # bit_length()는 정수의 이진 표현 비트 수 → log2(n)의 정수 근사값
    depth_limit = 2 * len(arr).bit_length()

    introsort(arr, 0, len(arr) - 1, depth_limit)
    return arr


# ── 테스트 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        [5, 2, 4, 6, 1, 3],
        [1, 2, 3, 4, 5],       # best case: 이미 정렬됨
        [5, 4, 3, 2, 1],       # worst case (퀵소트 기준): 역순
        [3, 1, 2, 3, 1],       # 중복 포함
        list(range(20, 0, -1)) # 크기 20, 역순
    ]

    for tc in test_cases:
        original = tc.copy()
        result = sort(tc)
        print(f"{original}\n→ {result}\n")
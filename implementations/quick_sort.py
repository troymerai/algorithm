"""
=============================================================
 퀵 정렬 (Quick Sort) 구현 가이드
=============================================================
 핵심 아이디어:
   분할 정복 — 피벗(pivot)을 기준으로
   작은 것은 왼쪽, 큰 것은 오른쪽으로 분할

 시간복잡도:
   Best    : O(n log n)  ← 피벗이 항상 중앙값
   Average : Θ(n log n)  ← 작년 문제 (3)번: 참
   Worst   : O(n²)       ← 이미 정렬된 배열 + 첫/끝 피벗

 공간복잡도: O(log n) ~ O(n) — 재귀 호출 스택
 안정성:     Unstable (피벗 교환 시 순서 깨질 수 있음)

 시험 포인트:
   - 작년 문제 (15)번: Ω(n)이라고 표현 가능? → 참
     (Ω는 하한이므로, n log n >= n 이니 Ω(n)도 성립) => n log n은 적어도 n 보다는 빠르게 증가
   - 평균이 n log n이지만 최악이 n²인 이유를 설명할 수 있어야 함
=============================================================
"""


def quick_sort(arr):

    if len(arr) <= 1:
        return arr
    
    pivot = arr[-1]  # 마지막 원소를 피벗으로
    
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    
    return quick_sort(left) + [pivot] + quick_sort(right)


def quick_sort_inplace(arr, low, high):
    """
    In-place 버전 (시험용 핵심)
    의사코드와 가장 유사한 형태
    """
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)   # 피벗 왼쪽
        quick_sort_inplace(arr, pivot_idx + 1, high)   # 피벗 오른쪽


def partition(arr, low, high):
    """
    Lomuto 파티션 방식
    
    피벗 = arr[high] (마지막 원소)
    i = 피벗보다 작은 구간의 끝 인덱스
    
    예시: arr = [3, 6, 8, 10, 1, 2, 1], pivot = 1(마지막)
    
    [3, 6, 8, 10, 1, 2, | 1]  pivot=1
     j→
    j=0: 3>1, skip
    j=1: 6>1, skip
    j=2: 8>1, skip
    j=3: 10>1, skip
    j=4: 1<=1, swap → i 증가
    j=5: 2>1, skip
    최종: 피벗을 i+1 위치로 교환
    """
    pivot = arr[high]
    i = low - 1           # 피벗보다 작은 구간의 끝
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # 피벗을 올바른 위치에 배치
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1



"""
─── 왜 최악이 O(n²)인가? ───

이미 정렬된 배열 [1, 2, 3, 4, 5]에서 마지막 원소를 피벗으로 선택:

1단계: pivot=5, left=[1,2,3,4], right=[]  → n-1번 비교
2단계: pivot=4, left=[1,2,3],   right=[]  → n-2번 비교
3단계: pivot=3, left=[1,2],     right=[]  → n-3번 비교
...

총 비교: (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n²)

1. pivot 선택 → O(1)  (그냥 맨 앞 원소 고름)
2. 파티셔닝   → O(n)  (pivot 기준으로 좌우 나누려고 전체 훑음)
1, 2를 n번 반복하니 O(n²)

→ 해결책: 랜덤 피벗 선택, 중앙값-of-3 등
"""


# ── 테스트 ──
if __name__ == "__main__":
    # 간결한 버전
    arr1 = [10, 7, 8, 9, 1, 5]
    print(f"간결: {arr1} → {quick_sort(arr1)}")
    
    # In-place 버전
    arr2 = [10, 7, 8, 9, 1, 5]
    quick_sort_inplace(arr2, 0, len(arr2) - 1)
    print(f"In-place: → {arr2}")
    
    # 최악의 경우
    arr3 = [1, 2, 3, 4, 5]
    print(f"최악(정렬됨): {arr3} → {quick_sort(arr3)}")
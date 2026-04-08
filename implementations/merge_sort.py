"""
=============================================================
 병합 정렬 (Merge Sort) 구현 가이드
=============================================================
 핵심 아이디어:
   분할 정복(Divide and Conquer)
   1) 배열을 반으로 나눈다 (Divide)
   2) 각 절반을 재귀적으로 정렬한다 (Conquer)
   3) 정렬된 두 배열을 합친다 (Combine)

 시간복잡도:
   Best / Average / Worst : 모두 Θ(n log n)
   → 항상 반으로 나누고, 합치는 데 O(n)이므로
   → 점화식: T(n) = 2T(n/2) + O(n)

 공간복잡도: O(n) — 임시 배열 필요 (In-place가 아님!)

 시험 포인트:
   - 작년 문제 (10)번: 병합 정렬은 내부 정렬(In-Place)? → 거짓!
   - 점화식 T(n) = 2T(n/2) + n 을 반복대치로 풀 줄 알아야 함
=============================================================
"""


def merge_sort(arr):
    """메인 함수: 배열을 반으로 나누고 재귀 호출"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # 왼쪽 절반 정렬
    right = merge_sort(arr[mid:])     # 오른쪽 절반 정렬
    
    return merge(left, right)          # 병합


def merge(left, right):
    """
    두 정렬된 배열을 하나로 합치기 (합치면서 정렬)
    
    예시:
    left  = [2, 5, 6]
    right = [1, 3, 4]
    
    비교 과정:
    2 vs 1 → 1 선택   result = [1]
    2 vs 3 → 2 선택   result = [1, 2]
    5 vs 3 → 3 선택   result = [1, 2, 3]
    5 vs 4 → 4 선택   result = [1, 2, 3, 4]
    나머지 추가        result = [1, 2, 3, 4, 5, 6]
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # <= 으로 해야 안정성 유지
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # 남은 원소들 추가
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


"""
─── 반복대치로 시간복잡도 유도 ───

점화식: T(n) = 2T(n/2) + cn

T(n) = 2T(n/2) + cn
     = 2[2T(n/4) + cn/2] + cn
     = 4T(n/4) + 2cn
     = 4[2T(n/8) + cn/4] + 2cn
     = 8T(n/8) + 3cn
     ...
     = 2^k · T(n/2^k) + k·cn

n/2^k = 1 일 때 k = log₂n

T(n) = n·T(1) + cn·log₂n
     = n + cn·log n
     = Θ(n log n)
"""


# ── 테스트 ──
if __name__ == "__main__":
    
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    print(f"방법1: {arr1} → {merge_sort(arr1)}")
    
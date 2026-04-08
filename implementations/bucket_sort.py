"""
=============================================================
 버킷 정렬 (Bucket Sort) 구현 가이드
=============================================================
 핵심 아이디어:
   1) 데이터 범위를 여러 구간(버킷)으로 나눈다
   2) 각 원소를 해당 버킷에 넣는다
   3) 각 버킷 내부를 정렬한다 (보통 삽입 정렬)
   4) 버킷을 순서대로 합친다

 시간복잡도:
   Best / Average : O(n + k)  ← k는 버킷 수, 균등 분포 시
   Worst          : O(n²)     ← 모든 원소가 한 버킷에 몰릴 때

 공간복잡도: O(n + k)
 안정성:     Stable (버킷 내부 정렬이 안정적이면)

 시험 포인트 (작년 문제 다수 출제):
   - (18)번: 실수일 때도 사용 가능? → 참
   - (19)번: 균등 분포일 때 가장 효율적? → 참
   - (20)번: 비교 기반 정렬이 필요 없다? → 거짓
     (버킷 내부에서 삽입 정렬 등 비교 기반 정렬 사용)
   - 9번: 버킷 수가 너무 적거나 많으면? (서술형)
=============================================================
"""


def insertion_sort_for_bucket(arr):
    """버킷 내부 정렬용 삽입 정렬"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bucket_sort_float(arr):
    """
    [0, 1) 범위의 실수 정렬 — 교과서 표준 버전

    예시: arr = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    
    버킷 10개 (0~9):
    bucket[0]: []
    bucket[1]: [0.17, 0.12]
    bucket[2]: [0.26, 0.21, 0.23]
    bucket[3]: [0.39]
    ...
    bucket[7]: [0.78, 0.72]
    bucket[9]: [0.94]
    
    각 버킷 내부 정렬 후 합치기
    """
    n = len(arr)
    if n <= 1:
        return arr
    
    # 1) n개의 빈 버킷 생성
    buckets = [[] for _ in range(n)]
    
    # 2) 각 원소를 적절한 버킷에 배분
    for x in arr:
        bucket_idx = int(n * x)        # [0,1) → [0, n-1]
        if bucket_idx == n:            # x가 정확히 1.0인 경우 방지
            bucket_idx = n - 1
        buckets[bucket_idx].append(x)
    
    # 3) 각 버킷 내부 정렬
    for bucket in buckets:
        insertion_sort_for_bucket(bucket)
    
    # 4) 버킷을 순서대로 합치기
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result


def bucket_sort_integer(arr):
    """
    일반 정수 배열용 버킷 정렬
    
    범위를 파악해서 버킷 수를 결정
    """
    if len(arr) <= 1:
        return arr
    
    n = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    
    # 버킷 수 = n (이상적: 원소 수와 같은 수의 버킷)
    bucket_count = n
    bucket_range = (max_val - min_val + 1) / bucket_count
    
    # 1) n개의 빈 버킷 생성
    buckets = [[] for _ in range(bucket_count)]
    
    # 2) 각 원소를 적절한 버킷에 배분
    for x in arr:
        idx = int((x - min_val) / bucket_range)
        if idx == bucket_count:
            idx -= 1
        buckets[idx].append(x)
    
    # 3) 각 버킷 내부 정렬 및 합치기
    result = []
    for bucket in buckets:
        insertion_sort_for_bucket(bucket)
        result.extend(bucket)
    
    return result


"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 시험 대비: 버킷 수에 따른 문제점 (작년 9번)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 버킷이 너무 적은 경우:
  - 각 버킷에 많은 원소가 들어감
  - 버킷 내부 정렬이 O(k²) (삽입 정렬)이므로 성능 저하
  - 극단적으로 버킷 1개 → 그냥 삽입 정렬과 동일 → O(n²)

■ 버킷이 너무 많은 경우:
  - 대부분의 버킷이 비어 있음 → 메모리 낭비
  - 빈 버킷을 순회하는 오버헤드 증가
  - 극단적으로 버킷 n²개 → 공간 낭비 O(n²)

■ 이상적인 버킷 수:
  - 일반적으로 n개 (원소 수와 동일)
  - 입력이 균등 분포면 각 버킷에 평균 1개 → O(n)
  - 핵심 조건: 각 버킷에 들어가는 원소 수가 상수에 가까워야 함
"""


# ── 테스트 ──
if __name__ == "__main__":
    # 실수 버전 [0, 1)
    float_arr = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print(f"실수: {float_arr}")
    print(f"  →   {bucket_sort_float(float_arr)}")
    
    # 정수 버전
    int_arr = [42, 32, 33, 52, 37, 47, 51]
    print(f"정수: {int_arr}")
    print(f"  →   {bucket_sort_integer(int_arr)}")
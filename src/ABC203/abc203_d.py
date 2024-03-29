'''
全ての区間の中央値が ${mid} 以上であるか否か を考えると、True, True, ..., True, False, False, ..., False のような分布になり、境目の True が今回求めたい最小値
(mid を大きくしていくと、どこかのタイミングで False になる)
↓
全ての区間の中央値をどうやって求めるか
↓
「x 番目に大きい値を中央値とする」という定義から、「区間内に、中央値より大きい値は X 個未満である」ことが分かる
↓
中央値を二分探索しながら、区間毎に中央値以上の値が x 個未満かどうかを判定する
↓
x 個未満の場合、その時検査した中央値は True のどれかになる
↓
で解けると思うが、実装では mid をどんどん小さくしていく方式でループしている
(mid がめちゃめちゃ大きいときにも exist = True になる)

'''
# 中央値の二分探索を行う
def run(n, k, _in):

    #ある区間の中で、[k*k/2] + 1 番目に大きい値を中央値とする、という定義
    #つまり、中央値が [k*k/2] + 1 番目に大きい = 中央値以上の値が、その区間には [k*k/2] + 1 個未満しかない、ということ
    limit = (k*k) // 2 + 1 

    ng = -1
    ok = 10**9 + 1

    # 今回の制約が N <= 800
    s = [[0 for i in range(n+1)] for j in range(n+1)]

    # ng は左終端、ok は右終端。二分探索の両端を条件に応じて狭めていく
    while ((ng + 1) < ok):
        exist = False
        mid = (ng + ok) // 2 # 明らかに今回の中央値は 0 以上 10**9 以下なので (各要素の上限が 10**9 だから)、最初は 10**9/2 で二分する
        for i in range(n):
            # 二次元累積和
            # 渡された中央値以上の _in[i][j] の個数を数え上げている (ある区間の中央値が x 以上 <=> ある区間に x 以上の値が半分以上存在する)
            for j in range(n): # 暗黙的に、 s[0][j] や s[i][0] などは 0
                s[i+1][j+1] = s[i+1][j] + s[i][j+1] - s[i][j] #最後の -s[i][j] は、重複分を減しているだけ
                if _in[i][j] > mid:
                    s[i+1][j+1] += 1

        # k*k の区間の選び方は (n-k+1)*(n-k+1) 通りある
        for i in range(n-k+1):
            for j in range(n-k+1):

                # ある k*k 区間で深さが mid 以上のマスの個数が limit 未満であるか否か = その区間の中央値が mid 以上であるか否か
                # ↑の解釈ちょっとおかしいな。。 例題をインプットとしたとき、例えば mid = 10000 とかだと exist = True になる。。

                if (s[i+k][j+k] + s[i][j] - s[i][j+k] - s[i+k][j] < limit): # ここの左辺って 0 にはならないのか。。
                    exist = True
        if exist:
            # 右終端を今回の mid に設定し、それより小さい中央値が存在するかどうかを次ループで検証する
            ok = mid
        else:
            ng = mid
    print(ok)

if __name__=="__main__":
    n,k = map(int, input().split())
    _in = []
    for _ in range(n):
        _in.append(list(map(int, input().split())))
    run(n, k, _in)
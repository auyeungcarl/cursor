public class HeapSort {
    public static void heapSort(int[] arr) {
        int n = arr.length;

        // 构建最大堆
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        // 一个个从堆顶取出元素
        for (int i = n - 1; i > 0; i--) {
            // 将堆顶元素（最大值）与末尾元素交换
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;

            // 对剩余元素重新构建最大堆
            heapify(arr, i, 0);
        }
    }

    // 将以 root 为根的子树调整为最大堆
    private static void heapify(int[] arr, int n, int root) {
        int largest = root;        // 初始化最大值为根节点
        int left = 2 * root + 1;   // 左子节点
        int right = 2 * root + 2;  // 右子节点

        // 如果左子节点大于最大值
        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }

        // 如果右子节点大于最大值
        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }

        // 如果最大值不是根节点
        if (largest != root) {
            // 交换根节点和最大值
            int temp = arr[root];
            arr[root] = arr[largest];
            arr[largest] = temp;

            // 递归调整被交换的子树
            heapify(arr, n, largest);
        }
    }

    // 测试代码
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        
        System.out.println("排序前的数组：");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        
        heapSort(arr);
        
        System.out.println("\n排序后的数组：");
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
} 
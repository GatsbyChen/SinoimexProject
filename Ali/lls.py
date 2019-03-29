# Definition for singly-linked list.
class Node(object):
    def __init__(self,x):
        self.val = x
        self.next = None

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        all_nums = []
        node_list = []
        for llists in lists:
            cur = llists[0]
            while cur == None:
                all_nums.append(cur.val)
                cur = cur.next
        sort_all_nums = sorted(all_nums)
        for nums in sort_all_nums:
            cur_node = Node(nums)
            node_list.append(cur_node)
        for nodes in node_list[:-1]:
            nodes.next = node_list[node_list.index(nodes)+1]
        return node_list[0]


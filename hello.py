def find_dominant_element(nums):
    candidate = None
    count = 0

    # Phase 1: Find a candidate for the majority element
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1

    # Phase 2: Verify the candidate
    if nums.count(candidate) > len(nums) // 2:
        return candidate
    else:
        return None


# Example usage
nums = [2, 2, 1, 1, 1, 2, 2]
dominant_element = find_dominant_element(nums)
print(
    f"The dominant element is: {dominant_element}"
    if dominant_element
    else "No dominant element found."
)

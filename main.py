def main():
    print("Hello World")
    return "Hello World"

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    try:
        result = main()
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

if __name__ == "__main__":
    main()
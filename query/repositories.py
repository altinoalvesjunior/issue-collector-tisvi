import requests
import utils.mongo

repositories_count = 0
endCursor = ""


def get_next_query(endcursor):
    next_query = """
    {
      search(
        type: REPOSITORY
        query: "pushed:>2020-02-01 topic:[INSERT YOUR STACK HERE] language:[INSERT LANGUAGE NAME HERE]"
        first: 25
        after: "%s"
      ) {
        nodes {
          ... on Repository {
            nameWithOwner
            name
            owner {
              login
            }
            stargazers {
              totalCount
            }
            url
            primaryLanguage {
              name
            }
            description
            openedIssues: issues(states: OPEN) {
              totalCount
            }
            closedIssues: issues(states: CLOSED) {
              totalCount
            }
            mergedPulls: pullRequests(states: MERGED) {
              totalCount
            }
            closedPulls: pullRequests(states: CLOSED) {
              totalCount
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """ % endcursor

    print('endcursor é: ' + endcursor)
    return next_query


def get_repositories():
    url = 'https://api.github.com/graphql'
    token = "[INSERT YOUR GITHUB TOKEN HERE]"
    headers = {"Authorization": "Bearer " + token}

    print('endcursor é (getRepositories): ' + endCursor)

    first_query = """
    {
      search(
        type: REPOSITORY
        query: "pushed:>2020-02-01 topic:[INSERT YOUR STACK HERE] language:[INSERT LANGUAGE NAME HERE]"
        first: 25
      ) {
        nodes {
          ... on Repository {
            nameWithOwner
            name
            owner {
              login
            }
            stargazers {
              totalCount
            }
            url
            primaryLanguage {
              name
            }
            description
            openedIssues: issues(states: OPEN) {
              totalCount
            }
            closedIssues: issues(states: CLOSED) {
              totalCount
            }
            mergedPulls: pullRequests(states: MERGED) {
              totalCount
            }
            closedPulls: pullRequests(states: CLOSED) {
              totalCount
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """

    request = requests.post(url, json={'query': first_query}, headers=headers)
    while repositories_count < 500:
        filter_repository(request)
        request = requests.post(url, json={'query': get_next_query(endCursor)}, headers=headers)


def filter_repository(request):
    json_response = request.json()
    json_count = len(json_response['data']['search']['nodes'])

    global endCursor
    endCursor = json_response['data']['search']['pageInfo']['endCursor']

    if json_count > 0:
        for i in range(json_count):
            repository = json_response['data']['search']['nodes'][i]

            def format_json(repo):
                return {
                    "name": repo["name"],
                    "nameWithOwner": repo["nameWithOwner"],
                    "owner": repo["owner"]["login"],
                    "stargazers": repo["stargazers"]["totalCount"],
                    "url": repo["url"],
                    "language": repo["primaryLanguage"]["name"],
                    "description": repo["description"],
                    "openedIssues": repo["openedIssues"]["totalCount"],
                    "closedIssues": repo["closedIssues"]["totalCount"],
                    "mergedPulls": repo["mergedPulls"]["totalCount"],
                    "closedPulls": repo["closedPulls"]["totalCount"],
                    "stack": "[INSERT YOUR STACK HERE]"
                }

            print(f' name: {repository["name"]}')
            repo_formatted = format_json(repository)
            utils.mongo.Mongo().insert_one_repository(repo_formatted)

            global repositories_count
            repositories_count += 1
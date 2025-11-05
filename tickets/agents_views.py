from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User

@api_view(['GET'])
def agents_list(request):
    try:
        agents = User.objects.filter(role__in=['Technical User', 'Technical Supervisor'])
        agent_data = []
        
        for agent in agents:
            agent_data.append({
                'id': agent.id,
                'name': agent.name,
                'email': agent.email,
                'role': agent.role
            })
        
        return Response(agent_data)
    except Exception as e:
        print(f"Error fetching agents: {e}")
        return Response([])
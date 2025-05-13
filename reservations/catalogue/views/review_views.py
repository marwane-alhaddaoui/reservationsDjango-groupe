from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalogue.models.review import Review
from catalogue.models.show import Show

class ShowReviewListView(APIView):
    def get(self, request, show_id):
        try:
            show = Show.objects.get(id=show_id)
            reviews = Review.objects.filter(show=show, validated=True)
            review_data = [
                {
                    "id": review.id,
                    "user": {"id": review.user.id, "username": review.user.username},
                    "review": review.review,
                    "stars": review.stars,
                    "created_at": review.created_at,
                }
                for review in reviews
            ]
            return Response(review_data, status=status.HTTP_200_OK)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)

class AllShowsReviewsView(APIView):
    def get(self, request):
        try:
            shows = Show.objects.all()
            data = []
            for show in shows:
                reviews = Review.objects.filter(show=show, validated=True)
                review_data = [
                    {
                        "id": review.id,
                        "user": {"id": review.user.id, "username": review.user.username},
                        "review": review.review,
                        "stars": review.stars,
                        "created_at": review.created_at,
                    }
                    for review in reviews
                ]
                data.append({
                    "show": {
                        "id": show.id,
                        "title": show.title,
                        "description": show.description,
                    },
                    "reviews": review_data
                })
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

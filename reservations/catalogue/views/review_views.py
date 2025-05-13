from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalogue.models.review import Review
from catalogue.models.show import Show
from rest_framework.authentication import TokenAuthentication


class ShowReviewListView(APIView):
    authentication_classes = [TokenAuthentication]
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
        

    def post(self, request, show_id):
        try:
            show = Show.objects.get(id=show_id)

            review_text = request.data.get('review')
            stars = request.data.get('stars')

            if not review_text or not stars:
                return Response({"error": "Review text and stars are required."}, status=status.HTTP_400_BAD_REQUEST)

            if not (1 <= int(stars) <= 5):
                return Response({"error": "Stars must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

            # Use the authenticated user
            review = Review.objects.create(
                show=show,
                user=request.user,
                review=review_text,
                stars=stars,
                validated=True  # Automatically validate for simplicity
            )
            return Response({"message": "Review added successfully.", "review_id": review.id}, status=status.HTTP_201_CREATED)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

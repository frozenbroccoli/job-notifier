import typing
import fastapi
import pydantic
from .. import linkedin
from .. import app


class SearchQueryParams(pydantic.BaseModel):
    keywords: str
    location: str
    distance: int = pydantic.Field(gt=0, le=50)
    job_type: typing.Literal['fullTime', 'partTime', 'contractual', 'internships', 'volunteer'] = 'fullTime'
    time_posted: typing.Literal['pastDay', 'pastWeek', 'pastMonth'] = 'pastDay'
    job_arrangements: list[typing.Literal['onSite', 'hybrid', 'remote']]
    num_results: int


class JobListings(pydantic.BaseModel):
    """
    Data model for job listings.
    """
    job_title: str
    job_url: pydantic.HttpUrl | None
    company_name: str
    location: str
    hiring_status: str
    posting_time: str


@app.get("/linkedin/job-listings/")
def get_linkedin_job_listings(queries: typing.Annotated[SearchQueryParams, fastapi.Query()]) -> list[JobListings]:
    return [JobListings(**listing) for listing in linkedin.get_job_listings(*[query[1] for query in queries])]

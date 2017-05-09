shell:
	docker-compose up -d runner; docker-compose run shell;

clean:
	docker-compose kill; docker-compose rm -f;

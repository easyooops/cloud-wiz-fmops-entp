from app.core.interface.service import Service

class DatabaseService(Service):
    def set_ready(self):
        """
        서비스를 준비 상태로 설정하는 메서드입니다.
        """
        print("DatabaseService is ready")

    def teardown(self):
        """
        서비스를 종료하고 리소스를 해제하는 메서드입니다.
        """
        print("DatabaseService is being torn down")

    def execute(self):
        """
        데이터베이스 서비스의 주요 로직을 실행하는 메서드입니다.
        """
        print("Executing DatabaseService logic")

#game manager, player 등 싱글톤 패턴을 적용시키기 위해 만들었습니다.
#이 클래스를 상속받으면 하나의 인스턴스만을 공유하게 할 수 있습니다.
class Singleton:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance
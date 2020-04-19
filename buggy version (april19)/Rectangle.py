class Rectangle:
    def getXBounds(self, points):
        point1 = [points[0], points[1]]
        point2 = [points[2], points[3]]
        point3 = [points[4], points[5]]
        point4 = [points[6], points[7]]
        return [point1[0], point3[0]]
    
    def getYBounds(self, points):
        point1 = [points[0], points[1]]
        point2 = [points[2], points[3]]
        point3 = [points[4], points[5]]
        point4 = [points[6], points[7]]
        return [point1[1], point3[1]]

    def contains(self, click, points):
        clickX = click[0]
        clickY = click[1]

        xBounds = Rectangle().getXBounds(points)
        yBounds = Rectangle().getYBounds(points)

        if (clickX >= xBounds[0] and clickX <= xBounds[1]):
            if (clickY >= yBounds[0] and clickY <= yBounds[1]):
                return True
        return False
